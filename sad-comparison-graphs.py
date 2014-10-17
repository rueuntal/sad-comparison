""" Project code for graphing the results of the comparisions for species abundance distribution (SAD) models """

from __future__ import division

import csv
import sys
import multiprocessing
import itertools
import os
import matplotlib.pyplot as plt
import colorsys
import numpy as np
from math import log, exp
from scipy import stats
import sqlite3 as dbapi

from mpl_toolkits.axes_grid.inset_locator import inset_axes


# Summarize the number of wins for each model/dataset
# Set up database capabilities 
# Set up ability to query data
con = dbapi.connect('./sad-data/SummarizedResults.sqlite')
cur = con.cursor()

# Switch con data type to string
con.text_factory = str




# Make histogram
# Set up figure
total_wins_fig= plt.figure()

# Extract number of wins for all datasets combined.
total_wins = cur.execute("""SELECT model_name, COUNT(model_code) AS total_wins FROM ResultsWin
                            GROUP BY model_code""")

total_wins = cur.fetchall()


# Plot variables for total wins
N = len(total_wins)
x = np.arange(1, N+1)
y = [ num for (s, num) in total_wins ]
labels = [ s for (s, num) in total_wins ]
width = 1
bar1 = plt.bar( x, y, width, color="grey" )
plt.ylabel( 'Number of Wins' )
plt.xticks(x + width/2.0, labels, fontsize = 'small' )
plt.xlabel( 'Species abundance distribution models' )


#Output figure
fileName = "./sad-data/total_wins.png"
plt.savefig(fileName, format="png" )




# Extract number of wins for each model and dataset
# BBS
bbs_wins  = cur.execute("""SELECT model_name, COUNT(model_code) AS total_wins FROM ResultsWin
                                 WHERE dataset_code == 'bbs'
                                 GROUP BY model_code""")
           
bbs_wins = cur.fetchall()

#CBC
cbc_wins = g= cur.execute("""SELECT model_name, COUNT(model_code) AS total_wins FROM ResultsWin
                                 WHERE dataset_code == 'cbc'
                                 GROUP BY model_code""")
           
cbc_wins = cur.fetchall()

#FIA
fia_wins = cur.execute("""SELECT model_name, COUNT(model_code) AS total_wins FROM ResultsWin
                                 WHERE dataset_code == 'fia'
                                 GROUP BY model_code""")
           
fia_wins = cur.fetchall()

#Gentry
gentry_wins = cur.execute("""SELECT model_name, COUNT(model_code) AS total_wins FROM ResultsWin
                                 WHERE dataset_code == 'gentry'
                                 GROUP BY model_code""")
           
gentry_wins = cur.fetchall()

#MCDB
mcdb_wins = cur.execute("""SELECT model_name, COUNT(model_code) AS total_wins FROM ResultsWin
                                 WHERE dataset_code == 'mcdb'
                                 GROUP BY model_code""")
           
mcdb_wins = cur.fetchall()

#NABA
naba_wins = cur.execute("""SELECT model_name, COUNT(model_code) AS total_wins FROM ResultsWin
                                 WHERE dataset_code == 'naba'
                                 GROUP BY model_code""")
           
naba_wins = cur.fetchall()

# Make histogram
# Set up figure
wins_by_dataset_fig = plt.figure()


# Plot variables for bbs subplot
plt.subplot(3,2,1)
N = len(bbs_wins)
x = np.arange(1, N+1)
y = [ num for (s, num) in bbs_wins ]
labels = [ s for (s, num) in bbs_wins ]
width = 1
bar1 = plt.bar( x, y, width, color="red" )
plt.yticks(fontsize = 'small')
plt.ylabel( 'Number of Wins', fontsize = 'small')
plt.xticks(x + width/2.0, labels, fontsize = 5.9 )
plt.xlabel( 'BBS' )


# Plot variables for cbc subplot
plt.subplot(3,2,2)
N = len(cbc_wins)
x = np.arange(1, N+1)
y = [ num for (s, num) in cbc_wins ]
labels = [ s for (s, num) in cbc_wins ]
width = 1
bar1 = plt.bar( x, y, width, color="orange" )
plt.yticks(fontsize = 'small')
plt.ylabel( 'Number of Wins', fontsize = 'small' )
plt.xticks(x + width/2.0, labels, fontsize = 5.9  )
plt.xlabel( 'CBC' )


# Plot variables for fia subplot
plt.subplot(3,2,3)
N = len(fia_wins)
x = np.arange(1, N+1)
y = [ num for (s, num) in fia_wins ]
labels = [ s for (s, num) in fia_wins ]
width = 1
bar1 = plt.bar( x, y, width, color="green" )
plt.yticks(fontsize = 'small')
plt.ylabel( 'Number of Wins', fontsize = 'small' )
plt.xticks(x + width/2.0, labels, fontsize = 5  )
plt.xlabel( 'FIA' )


# Plot variables for Gentry subplot
plt.subplot(3,2,4)
N = len(gentry_wins)
x = np.arange(1, N+1)
y = [ num for (s, num) in gentry_wins ]
labels = [ s for (s, num) in gentry_wins ]
width = 1
bar1 = plt.bar( x, y, width, color="olivedrab" )
plt.yticks(fontsize = 'small')
plt.ylabel( 'Number of Wins', fontsize = 'small' )
plt.xticks(x + width/2.0, labels, fontsize = 5.9  )
plt.xlabel( 'Gentry' )


# Plot variables for mcdb subplot
plt.subplot(3,2,5)
N = len(mcdb_wins)
x = np.arange(1, N+1)
y = [ num for (s, num) in mcdb_wins ]
labels = [ s for (s, num) in mcdb_wins ]
width = 1
bar1 = plt.bar( x, y, width, color="sienna" )
plt.yticks(fontsize = 'small')
plt.ylabel( 'Number of Wins', fontsize = 'small' )
plt.xticks(x + width/2.0, labels, fontsize = 5  )
plt.xlabel( 'MCDB' )



# Plot variables for NABA subplot
plt.subplot(3,2,6)
N = len(naba_wins)
x = np.arange(1, N+1)
y = [ num for (s, num) in naba_wins ]
labels = [ s for (s, num) in naba_wins ]
width = 1
bar1 = plt.bar( x, y, width, color="blue" )
plt.yticks(fontsize = 'small')
plt.ylabel( 'Number of Wins', fontsize = 'small' )
plt.xticks(x + width/2.0, labels, fontsize = 5.9  )
plt.xlabel( 'NABA' )

plt.tight_layout()


#Output figure
fileName = "./sad-data/wins_by_dataset.png"
plt.savefig(fileName, format="png" )



#AIC_c weight distributions graphs
# Make histogram
# Set up figure
AIC_c_weights = plt.figure()

# Extract AICc weights for each model.
logseries = cur.execute("""SELECT model_name, value FROM RawResults
                            WHERE model_name == 'Logseries' AND value_type =='AICc weight' AND value IS NOT NULL
                            ORDER BY value""")
logseries = cur.fetchall()


untruncated_logseries = cur.execute("""SELECT model_name, value FROM RawResults
                            WHERE model_name =='Untruncated logseries' AND value_type =='AICc weight' AND value IS NOT NULL
                            ORDER BY value""")
untruncated_logseries = cur.fetchall()


pln = cur.execute("""SELECT model_name, value FROM RawResults
                            WHERE model_name =='Poisson lognormal' AND value_type =='AICc weight' AND value IS NOT NULL
                            ORDER BY value""")
pln = cur.fetchall()
                              
                            
neg_bin = cur.execute("""SELECT model_name, value FROM RawResults
                            WHERE model_name =='Negative binomial' AND value_type =='AICc weight' AND value IS NOT NULL
                            ORDER BY value""")
neg_bin = cur.fetchall()
                      
                            
geometric = cur.execute("""SELECT model_name, value FROM RawResults
                            WHERE model_name =='Geometric series' AND value_type =='AICc weight' AND value IS NOT NULL
                            ORDER BY value""")
geometric = cur.fetchall()


# Plot variables for weights
bins = 50

model0 = [ num for (s, num) in logseries ]
plt.hist(model0, bins, range = (0,1), facecolor = 'magenta', histtype="stepfilled", alpha=1, label = "Truncated logseries")

model1 = [ num for (s, num) in untruncated_logseries]
plt.hist(model1, bins, range = (0,1), facecolor = 'orange', histtype="stepfilled", alpha=.7, label = "Untruncated logseries")

model2 = [ num for (s, num) in pln]
plt.hist(model2, bins, range = (0,1), facecolor = 'teal', histtype="stepfilled", alpha=.7, label = "Poisson lognormal")

model3 = [ num for (s, num) in neg_bin]
plt.hist(model3, bins, range = (0,1), facecolor = 'gray', histtype="stepfilled", alpha=.7, label = "Negative binomial")

model4 = [ num for (s, num) in geometric]
plt.hist(model4, bins, range = (0,1), facecolor = 'olivedrab', histtype="stepfilled", alpha=.7, label = "Geometric")

plt.legend(loc = 'upper right', fontsize = 11)

plt.xlabel("AICc weights")
plt.ylabel("Frequency")

plt.tight_layout()



#Output figure
fileName = "./sad-data/AICc_weights.png"
plt.savefig(fileName, format="png" )

# Plot weights for each model individually
bins = 50

# Set up figures
plt.figure()
plt.hist(model0, bins, range = (0,1), facecolor = 'magenta', histtype="stepfilled", alpha=1, label = "Truncated logseries")
plt.xlabel("Truncated logseries AICc weights")
plt.ylabel("Frequency")

plt.tight_layout()

#Output figure
fileName = "./sad-data/Truncated_logseries_weights.png"
plt.savefig(fileName, format="png" )

plt.figure()
plt.hist(model1, bins, range = (0,1), facecolor = 'orange', histtype="stepfilled", alpha=.7, label = "Untruncated logseries")
plt.xlabel("Untruncated logseries AICc weights")
plt.ylabel("Frequency")

plt.tight_layout()

#Output figure
fileName = "./sad-data/Untruncated logseries_weights.png"
plt.savefig(fileName, format="png" )


plt.figure()
plt.hist(model2, bins, range = (0,1), facecolor = 'teal', histtype="stepfilled", alpha=.7, label = "Poisson lognormal")
plt.xlabel("Poisson lognormal AICc weights")
plt.ylabel("Frequency")

plt.tight_layout()

#Output figure
fileName = "./sad-data/Poisson lognormal_weights.png"
plt.savefig(fileName, format="png" )


plt.figure()
model3 = [ num for (s, num) in neg_bin]
plt.hist(model3, bins, range = (0,1), facecolor = 'gray', histtype="stepfilled", alpha=.7, label = "Negative binomial")
plt.xlabel("Negative binomial AICc weights")
plt.ylabel("Frequency")

plt.tight_layout()

#Output figure
fileName = "./sad-data/Negative binomial_weights.png"
plt.savefig(fileName, format="png" )


plt.figure()
model4 = [ num for (s, num) in geometric]
plt.hist(model4, bins, range = (0,1), facecolor = 'olivedrab', histtype="stepfilled", alpha=.7, label = "Geometric")

plt.xlabel("Geometric AICc weights")
plt.ylabel("Frequency")

plt.tight_layout()

#Output figure
fileName = "./sad-data/Geometric_weights.png"
plt.savefig(fileName, format="png" )


#Likelihood graph
# Make histogram
# Set up figure
l_likelihood = plt.figure()

# Extract log-likelihoods for each model.
ll_logseries = cur.execute("""SELECT model_name, value FROM RawResults
                            WHERE model_name == 'Logseries' AND value_type =='likelihood' AND value IS NOT NUll
                            ORDER BY value""")
ll_logseries = cur.fetchall()


ll_untruncated_logseries = cur.execute("""SELECT model_name, value FROM RawResults
                            WHERE model_name =='Untruncated logseries' AND value_type =='likelihood' AND value IS NOT NUll
                            ORDER BY value""")
ll_untruncated_logseries = cur.fetchall()



ll_pln = cur.execute("""SELECT model_name, value FROM RawResults
                            WHERE model_name =='Poisson lognormal' AND value_type =='likelihood' AND value IS NOT NUll
                            ORDER BY value""")
ll_pln = cur.fetchall()
                     
                            
                            
ll_neg_bin = cur.execute("""SELECT model_name, value FROM RawResults
                            WHERE model_name =='Negative binomial' AND value_type =='likelihood' AND value IS NOT NUll
                            ORDER BY value""")
ll_neg_bin = cur.fetchall()


                      
                            
ll_geometric = cur.execute("""SELECT model_name, value FROM RawResults
                            WHERE model_name =='Geometric series' AND value_type =='likelihood' AND value IS NOT NUll 
                            ORDER BY value""")
ll_geometric = cur.fetchall()



# Plot variables for weights
bins = 50

ll_model0 = [ num for (s, num) in ll_logseries ]
plt.hist(ll_model0, bins, facecolor = 'magenta', histtype="stepfilled", alpha=1, label = "Truncated logseries")

ll_model1 = [ num for (s, num) in ll_untruncated_logseries]
plt.hist(ll_model1, bins, facecolor = 'orange', histtype="stepfilled", alpha=.7, label = "Untruncated logseries")

ll_model2 = [ num for (s, num) in ll_pln]
plt.hist(ll_model2, bins, facecolor = 'teal', histtype="stepfilled", alpha=.7, label = "Poisson lognormal")

ll_model3 = [ num for (s, num) in ll_neg_bin]
plt.hist(ll_model3, bins, facecolor = 'gray', histtype="stepfilled", alpha=.7, label = "Negative binomial")

ll_model4 = [ num for (s, num) in ll_geometric]
plt.hist(ll_model4, bins, facecolor = 'olivedrab', histtype="stepfilled", alpha=.7, label = "Geometric")

plt.legend(loc = 'upper left', fontsize = 11)

plt.xlabel("Log-likelihoods")
plt.ylabel("Frequency")

plt.tight_layout()

#Output figure
fileName = "./sad-data/likelihoods.png"
plt.savefig(fileName, format="png" )

# Plot likelihoods for each model individually
#Truncated logseries
plt.figure()
plt.hist(ll_model0, bins, facecolor = 'magenta', histtype="stepfilled", alpha=1, label = "Truncated logseries")
plt.xlabel("Truncated logseries log-likelihoods")
plt.ylabel("Frequency")

plt.tight_layout()

#Output figure
fileName = "./sad-data/truncated_logseries_likelihoods.png"
plt.savefig(fileName, format="png" )


#Untruncated logseries
plt.figure()
plt.hist(ll_model1, bins, facecolor = 'orange', histtype="stepfilled", alpha=.7, label = "Untruncated logseries")
plt.xlabel("Untruncated logseries log-likelihoods")
plt.ylabel("Frequency")

plt.tight_layout()

#Output figure
fileName = "./sad-data/untruncated_logseries_likelihoods.png"
plt.savefig(fileName, format="png" )

#Poisson lognormal
plt.figure()
plt.hist(ll_model2, bins, facecolor = 'teal', histtype="stepfilled", alpha=.7, label = "Poisson lognormal")
plt.xlabel("Poisson lognormal log-likelihoods")
plt.ylabel("Frequency")

plt.tight_layout()

#Output figure
fileName = "./sad-data/pln_likelihoods.png"
plt.savefig(fileName, format="png" )

#Negative binomial
plt.figure()
plt.hist(ll_model3, bins, facecolor = 'gray', histtype="stepfilled", alpha=.7, label = "Negative binomial")
plt.xlabel("Negative binomial log-likelihoods")
plt.ylabel("Frequency")

plt.tight_layout()

#Output figure
fileName = "./sad-data/neg_bin_likelihoods.png"
plt.savefig(fileName, format="png" )

#Geometric
plt.figure()
plt.hist(ll_model4, bins, facecolor = 'olivedrab', histtype="stepfilled", alpha=.7, label = "Geometric")
plt.xlabel("Geometric log-likelihoods")
plt.ylabel("Frequency")

plt.tight_layout()

#Output figure
fileName = "./sad-data/geometric_likelihoods.png"
plt.savefig(fileName, format="png" )


# Close connection
con.close()
