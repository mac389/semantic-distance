import numpy as np

from src.analysis import visualization
from sklearn.decomposition import PCA



def load(filename):
	data = np.memmap(filename,dtype='float32',mode='r')
	return np.reshape(data,(np.sqrt(data.shape),-1))

data = load('./data/test-similarity-matrix.npy')

pca = PCA(n_components=5)
data_r = pca.fit(data).transform(data)

print 'Explained variance ratio for 1st 5 components: %s'%str(pca.explained_variance_ratio_)