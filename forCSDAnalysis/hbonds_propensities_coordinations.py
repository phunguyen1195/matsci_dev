#!/usr/bin/env python
# coding: utf-8

# In[48]:


import ccdc
import os
import sys
import csv
import argparse
import pandas as pd
from tabulate import tabulate
from ccdc.descriptors import CrystalDescriptors
import glob
from ccdc import crystal
#############################################################################################
folder = "/home/phunguyen/forCSDAnalysis/Exp/"
dest = "/home/phunguyen/Documents/CDSana/output_Exp.csv"
dest2 = "/home/phunguyen/Documents/CDSana/output_Exp.txt"
calculator = CrystalDescriptors.HBondCoordination()
print (calculator.settings.hbond_criterion.distance_range)
print (calculator.settings.hbond_criterion.path_length_range)
calculator.settings.hbond_criterion.distance_range = (-5, 1.0)
calculator.settings.hbond_criterion.vdw_corrected = True
calculator.settings.hbond_criterion.path_length_range = (-1,999)
hbp = CrystalDescriptors.HBondPropensities()
path_list = glob.glob(folder +'*.cif')
reader = []
path_name = []
for path in path_list:
    with open(path) as f:
        s = f.read()
    reader.append(crystal.Crystal.from_string(s,format='cif'))
    path_name.append(os.path.basename(path))
df_raw = pd.DataFrame(data={"Path_name" : path_name, "reader" : reader})
identifier = []
number_hbond_observed = []
detail_observed = []
propensities = []
row_name = []
for index, row in df_raw.iterrows():
     c = row["reader"]
     print (c.hbonds())
     #GSA = CrystalDescriptors.GraphSetSearch()
     #default_gsets = GSA.search(c)
     #GSA.settings.distance_range = (-5, 1.0)
     if c.has_disorder:
	print(row["Path_name"])
        continue
     try:
	 row_name.append(row["Path_name"])
         hbp.set_target(c)
         funtional = []
         donors = []
         acceptors = []
         for j in hbp.functional_groups:
             funtional.append(j.identifier)
         for d in hbp.donors:
             donors.append(d.identifier)
         for a in hbp.acceptors:
             acceptors.append(a.identifier)
         df_pen = pd.concat([pd.DataFrame({"functional groups": funtional}),pd.DataFrame({"donors":donors}),pd.DataFrame({"acceptors": acceptors})], axis = 1)
         df_pen.reset_index(drop=True)
         propensities.append(pd.concat([pd.DataFrame({"functional groups": funtional}),pd.DataFrame({"donors":donors}),pd.DataFrame({"acceptors": acceptors})], axis = 1))
     except Exception as e:
         print (path_list[reader.index(c)])
	 print (row["Path_name"])
         print (e)
         propensities.append(pd.DataFrame({"functional groups": [], "donors": [], "acceptors": []}))
     predictions = calculator.predict(c)
     print (calculator.settings.hbond_criterion.distance_range)
     print (calculator.settings.hbond_criterion.path_length_range)
     identifier.append(c.identifier)
     number_hbond_observed.append(len(predictions.observed))
     label = []
     p = []
     coordination = []
     for i in predictions.observed:
         label.append(i.label)
         p.append(i.probability)
         coordination.append(i.coordination_count)
	 #print (settings.distance_range)
	 df_coordination = pd.DataFrame(data= {"label" : label, "coordination count": coordination, "probability": p})
	 df_coordination.sort_values('probability', inplace=True, ascending=False)
     detail_observed.append(df_coordination)

df = pd.DataFrame(data={"name": row_name,"identifiers" : identifier, "number of hbonds observed" : number_hbond_observed, "detail observed" : detail_observed, "Propensities": propensities})

with pd.option_context('display.max_rows', 10000000000):
    file = open(dest2, 'w')
    file.write (tabulate(df, headers='keys', tablefmt='psql'))
    file.close()
df.to_csv(dest)


# In[ ]:




