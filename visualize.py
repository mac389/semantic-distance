import os, json, matplotlib 
matplotlib.use('Agg')

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd 

READ = 'rb'
directory = json.load(open('directory.json',READ))		
filename = os.path.join(directory['data-prefix'],'test-similarity-matrix.npy')


data = np.load(filename).astype(float)
data  = (data-data.min())/(data.max()-data.min()) #Think more about how to scale

f,ax = plt.subplots(figsize=(12,9))

#Only for control

color_series = {i:color for i,color in enumerate(sns.color_palette("husl", 3))}
colors = pd.Series([color_series[i%3] for i in xrange(data.shape[0])])
print colors

hmap = sns.clustermap(np.corrcoef(data),col_colors = colors,row_colors=colors)
#plt.tight_layout()
plt.savefig('./results/clustermap-corr2.png')