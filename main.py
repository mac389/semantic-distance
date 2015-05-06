import itertools,json,os, string

import numpy as np
import src.nlp.utils as tech

from src.nlp.SemanticString import SemanticString
from progress.bar import Bar
from optparse import OptionParser
from random import sample
from nltk import FreqDist,pos_tag

READ = 'rb'
WRITE = 'wb'
ERROR_CODE = -1
directory = json.load(open('directory.json',READ))		
stopwords = set([word.rstrip('\r\n').strip() for word in open(directory['stopwords'],READ).readlines()])
emoticons = set([word.rstrip('\r\n').strip() for word in open(directory['emoticons'],READ).readlines()])
punctuation = set(string.punctuation) 
 
#--Load input from command line
op = OptionParser()
op.add_option('--f', dest='corpus', type='str', help='Corpus of data on which to process semantic distance')
op.add_option('--r', dest='random_sample',type='int',help='Percentage of sample to calculate',default=100)
op.add_option('--i',action="store_true", dest="inspect")
op.print_help()

opts,args = op.parse_args()
if len(args) > 0:
	op.error('This script only takes arguments preceded by command line options.')

if not opts.corpus:
	opts.corpus = 'test'
	print 'No file passed. Using test text.'


corpus = open(opts.corpus,READ).read().splitlines() #Assumes each phrase occupies one line
corpus = [[(word,pos) for word,pos in pos_tag(tech.word_tokenize(phrase)) 
				if not any([word in verboten for verboten in [stopwords,emoticons,punctuation]])]
				for phrase in corpus]

words,_ = zip(*list(itertools.chain.from_iterable(corpus)))
freqs = FreqDist(words)
filename = os.path.join(directory['data-prefix'],'%s-similarity-matrix.npy'%(opts.corpus.split('.')[0]))

with open('.gitignore','a+') as f:
	print>>f,filename

database = json.load(open(directory['database'],READ))

if opts.random_sample < 100:
	corpus = sample(corpus,int(opts.random_sample/float(100)*len(corpus)))

#Remove non-English tweets <--TODO
print 'Creating array'
similarity = np.zeros((len(corpus),len(corpus)))
#similarity = np.memmap(filename,dtype='float32',mode='w+', shape=(len(corpus),len(corpus))).astype(int)
#TODO filter out words with low tf-idf <-- Does this make sense?
if not opts.inspect:
	bar = Bar('Calulating semantic distance', max=len(corpus)*(len(corpus)-1)/2)
for i in xrange(len(corpus)):
	for j in xrange(i):
		distance = SemanticString(corpus[i],database,inspect=opts.inspect) - SemanticString(corpus[j],database,inspect=opts.inspect)
		similarity[i,j] = ERROR_CODE if np.isnan(distance) else int(1000*(distance))
 		if not opts.inspect:
	 		bar.next()
if not opts.inspect:
	bar.finish()

json.dump(database,open(filename,WRITE))	
similarity += similarity.transpose()
#np.savetxt('%s.similarity-matrix-tsv'%(self.filenames['corpus'].rstrip('.txt')),self.M,fmt='%.04f',delimiter='\t')
np.save(filename,similarity) #Del also flushes a memmap to disk
print 'Saved as %s'%filename
if opts.inspect:
	tech.printmat(similarity,row_labels=corpus,col_labels=corpus)
