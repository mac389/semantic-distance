import itertools,json,os

from src.nlp.SemanticString import SemanticString
from nltk.corpus import wordnet
from nltk import word_tokenize, pos_tag
from progress.bar import Bar
from optparse import OptionParser
from random import sample

import numpy as np

READ = 'rb'
WRITE = 'wb'

directory = json.load(open('directory.json',READ))		


#--Command  line parsing
op = OptionParser()
op.add_option('--f', dest='corpus', type='str', help='Corpus of data on which to process semantic distance')
op.add_option('--r', dest='random_sample',type='int',help='Percentage of sample to calculate')
op.print_help()

opts,args = op.parse_args()
if len(args) > 0:
	op.error('This script only takes arguments preceded by command line options.')

if not opts.corpus:
	opts.corpus = 'test'
	print 'No file passed. Using test text.'


filename = os.path.join(directory['data-prefix'],'%s-similarity-matrix.npy'%(opts.corpus.split('.')[0]))
database = json.load(open(directory['database'],READ))

with open(opts.corpus) as f:
	corpus = [string.strip() for string in f.readlines()]

if opts.random_sample < 100:
	corpus = sample(corpus,int(opts.random_sample/float(100)*len(corpus)))

#Remove non-English tweets

print 'Creating array'
#self.similarity = np.zeros((len(self.corpus),len(self.corpus)))
similarity = np.memmap(filename,dtype='float32',mode='w+', shape=(len(corpus),len(corpus)))
#TODO filter out words with low tf-idf <-- Does this make sense?


bar = Bar('Calulating semantic distance', max=len(corpus)*(len(corpus)+1)/2)
for i in xrange(len(corpus)):
	for j in xrange(i):

		if corpus[i] == corpus[j]:
			similarity[i,j] = 1
		else:
	 		similarity[i,j] = SemanticString(corpus[i],database) - SemanticString(corpus[j],database)
 		bar.next()
	bar.next()
bar.finish()

json.dump(database,open(directory['data-prefix'],WRITE))	

similarity += similarity.transpose()
similarity[np.diag_indices(len(corpus))] = 1

#np.savetxt('%s.similarity-matrix-tsv'%(self.filenames['corpus'].rstrip('.txt')),self.M,fmt='%.04f',delimiter='\t')
del similarity #Del also flushes a memmap to disk