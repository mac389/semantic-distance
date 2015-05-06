import numpy as np
import cPickle
import visualization.Graphics as artist
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler


from matplotlib import rcParams

rcParams['text.usetex'] = True

data = np.memmap('../data/alcohol_shor.similarity-matrix-tsv',dtype='float32',mode='r',shape=(200,200))