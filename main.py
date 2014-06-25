import itertools,json,os

from src.SemanticString import SemanticString
from nltk.corpus import wordnet
from nltk import word_tokenize, pos_tag
from progress.bar import Bar
from optparse import OptionParser

import numpy as np

READ = 'rb'
WRITE = 'wb'

directory = json.load(open('directory.json',READ))		


#--Command  line parsing
op = OptionParser()
op.add_option('--f', dest='corpus', type='str', help='Corpus of data on which to process semantic distance')
op.print_help()
#

opts,args = op.parse_args()
if len(args) > 0:
	op.error('This script only takes arguments preceded by command line options.')
	sys.exit(1)

filename = os.path.join(directory['data-prefix'],'%s.similarity-matrix-tsv'%(opts.corpus.rstrip('.txt')))
database = json.load(directory['database'],self.READ)

with open(opts.corpus) as f:
	corpus = [string.strip() for string in f.readlines()]

#Remove non-English tweets

print 'Creating array'
#self.similarity = np.zeros((len(self.corpus),len(self.corpus)))
similarity = np.memmap(self.filename,dtype='float32',mode='w+', shape=(len(corpus),len(corpus)))
#TODO filter out words with low tf-idf <-- Does this make sense?


bar = Bar('Calulating semantic distance', max=len(corpus)*(len(corpus)+1)/2)
for i in xrange(len(self.corpus)):
	for j in xrange(i):

 		similarity[i,j] = SemanticString(corpus[i],database) - SemanticString(corpus[j],database)

 		bar.next()
	bar.next()
bar.finish()

json.dump(database,open(directory['database'],WRITE))	

similarity += self.similarity.transpose()
similarity[np.diag_indices(len(self.corpus))] = 1
#np.savetxt('%s.similarity-matrix-tsv'%(self.filenames['corpus'].rstrip('.txt')),self.M,fmt='%.04f',delimiter='\t')
del similarity #Del also flushes a memmap to disk