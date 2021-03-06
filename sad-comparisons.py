""" Project code for comparing species abundance distribution (SAD) models

To run this code:

python sad-comparisons.py

To use a non-standard data directory:

python sad-comparisons.py /path/to/data_dir

To run data sets other than the default publicly available data add a file to
the data directory (`./sad-data` by default) named `dataset_config.txt` that
contains a list of dataset names, one on each line.

This code depends on the most recent version of the macroecotools Python
module, which can be installed directly from github using pip:

pip install git+https://github.com/weecology/macroecotools.git

"""

from __future__ import division

import csv
import numpy as np
import os
import sys
from math import log, exp

from pandas import DataFrame

import macroecotools
import macroeco_distributions as md

def import_abundance(datafile):
    """Imports raw species abundance .csv files in the form: Site, Year, Species, Abundance."""
    raw_data = np.genfromtxt(datafile, dtype = "S15,i8,S50,i8", names = ['site','year','sp','ab'], delimiter = ",",comments = "#")
    return raw_data

def model_comparisons(raw_data, dataset_name, data_dir, cutoff = 9):
    """ Uses raw species abundance data to compare predicted vs. empirical species abundance distributions (SAD) and output results in csv files. 
    
    Keyword arguments:
    raw_data: numpy structured array with 4 columns: 'site', 'year', 'sp' (species), 'ab' (abundance).
    dataset_name: short code to indicate the name of the dataset in the output file names.
    data_dir: directory in which to store results output.
    cutoff: minimum number of species required to run -1.
    
    SAD models and packages used:
    Logseries (macroecotools/macroecodistributions)
    Poisson lognormal (macroecotools/macroecodistributions)
    Negative binomial (macroecotools/macroecodistributions)
    Zipf (macroecotools/macroecodistributions)
    
    Neutral theory: Neutral theory predicts the negative binomial distribution (Connolly et al. 2014. Commonness and rarity in the marine biosphere. PNAS 111: 8524-8529. http://www.pnas.org/content/111/23/8524.abstract
    
    """
    usites = np.sort(np.unique(raw_data["site"]))
    
    # Open output files
    f1 = open(data_dir + dataset_name + '_dist_test.csv','wb')
    output1 = csv.writer(f1)
    f2 = open(data_dir + dataset_name + '_likelihoods.csv','wb')
    output2 = csv.writer(f2)
    f3 = open(data_dir + dataset_name + '_relative_L.csv','wb')
    output3 = csv.writer(f3)
   
    # Insert header
    output1.writerow(['site', 'S', 'N', 'AICc_logseries', 'AICc_pln', 'AICc_negbin', 'AICc_zipf'])
    output2.writerow(['site', 'S', 'N', 'likelihood_logseries', 'likelihood_pln', 'likelihood_negbin', 'likelihood_zipf'])
    output3.writerow(['site', 'S', 'N', 'relative_ll_logseries', 'relative_ll_pln', 'relative_ll_negbin', 'relative_ll_zipf'])    

    results = []
    for site in usites:
        subsites = raw_data["site"][raw_data["site"] == site]        
        subabundance = raw_data["ab"][raw_data["site"] == site]
        N = sum(subabundance) # N = total abundance for a site
        S = len(subsites) # S = species richness at a site
        if (min(subabundance) > 0) and (S > cutoff):
            print("%s, Site %s, S=%s, N=%s" % (dataset_name, site, S, N))
                        
            # Calculate Akaike weight of species abundance models:
            # Parameter k is the number of fitted parameters
            k1 = 1
            k2 = 2            
            
            # Calculate log-likelihoods of species abundance models and calculate AICc values:
            # Logseries
            p_untruncated = md.logser_solver(subabundance)
            L_logser_untruncated = md.logser_ll(subabundance, p_untruncated) # Log-likelihood of untruncated logseries
            AICc_logser_untruncated = macroecotools.AICc(k1, L_logser_untruncated, S) # AICc logseries untruncated
            relative_ll_logser_untruncated = AICc_logser_untruncated# Relative likelihood untruncated logseries
            
            #Start making AICc list
            AICc_list = [AICc_logser_untruncated]
            likelihood_list = [L_logser_untruncated]
            relative_likelihood_list = [relative_ll_logser_untruncated]          
            
            # Poisson lognormal
            mu, sigma = md.pln_solver(subabundance)
            L_pln = md.pln_ll(subabundance, mu,sigma) # Log-likelihood of Poisson lognormal
            AICc_pln = macroecotools.AICc(k2, L_pln, S) # AICc Poisson lognormal
            relative_ll_pln = macroecotools.AICc(k1, L_pln, S) #Relative likelihood, Poisson lognormal
            # Add to AICc list
            AICc_list = AICc_list + [AICc_pln]
            likelihood_list = likelihood_list +  [L_pln]
            relative_likelihood_list = relative_likelihood_list + [relative_ll_pln]
       
            # Negative binomial
            n0, p0 = md.nbinom_lower_trunc_solver(subabundance)
            L_negbin = md.nbinom_lower_trunc_ll(subabundance, n0, p0) # Log-likelihood of negative binomial
            AICc_negbin = macroecotools.AICc(k2, L_negbin, S)# AICc negative binomial
            relative_ll_negbin = macroecotools.AICc(k1, L_negbin, S) # Relative log-likelihood of negative binomial
            # Add to AICc list
            AICc_list = AICc_list + [AICc_negbin]
            likelihood_list = likelihood_list +  [L_negbin]
            relative_likelihood_list = relative_likelihood_list + [relative_ll_negbin]
            
            # Zipf distribution
            par = md.zipf_solver(subabundance)
            L_zipf = md.zipf_ll(subabundance, par) #Log-likelihood of Zipf distribution
            AICc_zipf = macroecotools.AICc(k1, L_zipf, S)
            relative_ll_zipf = AICc_zipf
            #Add to AICc list
            AICc_list = AICc_list + [AICc_zipf]
            likelihood_list = likelihood_list +  [L_zipf]
            relative_likelihood_list = relative_likelihood_list + [relative_ll_zipf]            
            
            # Calculate AICc weight            
            weight = macroecotools.aic_weight(AICc_list, S, cutoff = 4)
            
            #Calculate relative likelihood
            relative_likelihoods = macroecotools.aic_weight(relative_likelihood_list, S, cutoff = 4)
            
            # Convert weight to list
            weights_output = weight.tolist()
            
            #Convert relative likelihoods to list
            relative_likelihoods_output = relative_likelihoods.tolist() 
                                                
            # Format results for output
            for weight in weights_output:
                results1 = [[site, S, N] + weights_output]
            results2 = [[site, S, N] + likelihood_list]
            results3 = [[site, S, N] + relative_likelihoods_output]
            results.append([site, S, N] + weights_output  + likelihood_list + relative_likelihoods_output)

            # Save results to a csv file:
            output1.writerows(results1)
            output2.writerows(results2)
            output3.writerows(results3)

    results = DataFrame(results, columns=['site', 'S', 'N', 'AICc_logseries', 'AICc_pln', 'AICc_negbin',
                                         'AICc_zipf', 'likelihood_logseries', 'likelihood_pln',
                                         'likelihood_negbin', 'likelihood_zipf', 'relative_ll_logseries',
                                         'relative_ll_pln', 'relative_ll_negbin', 'relative_ll_zipf'])
    results.to_csv(os.path.join(data_dir, dataset_name +  '_likelihood_results.csv'), index=False)
    f1.close()
    f2.close()
    f3.close()           


if __name__ == '__main__':
    # Set up analysis parameters
    analysis_ext = '_spab.csv' # Extension for raw species abundance files

    if len(sys.argv) > 1:
        data_dir = sys.argv[1]
    else:
        data_dir = './sad-data/'

    #Determine which datasets to use
    if os.path.exists(data_dir + 'dataset_config.txt'):
        dataset_config_file = open(data_dir + 'dataset_config.txt', 'r')
        datasets = []
        for line in dataset_config_file:
            datasets.append(line.strip())
    else:
        datasets = ['bbs', 'fia', 'gentry', 'mcdb']
    
    # Starts actual analyses for each dataset in turn.
    for dataset in datasets:
        datafile = data_dir + dataset + analysis_ext
            
        raw_data = import_abundance(datafile) # Import data
    
        model_comparisons(raw_data, dataset, data_dir, cutoff = 9) # Run analyses on data
