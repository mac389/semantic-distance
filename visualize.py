import os, json, matplotlib 
matplotlib.use('Agg')

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd 

READ = 'rb'
directory = json.load(open('directory.json',READ))		
filename = os.path.join(directory['data-prefix'],'test-similarity-matrix.npy')


data = np.load(filename)
f,ax = plt.subplots(figsize=(12,9))

hmap = sns.clustermap(np.corrcoef(data))

#plt.tight_layout()
plt.savefig('./results/clustermap-corr.png')