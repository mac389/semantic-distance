import itertools,json

import numpy as np

from nltk.corpus import wordnet
from nltk.corpus import wordnet_ic
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import FreqDist

from pprint import pformat
from termcolor import colored

from SemanticParser import SemanticParser

brown_ic = wordnet_ic.ic('ic-brown.dat')

morphy_tag = {'NN':wordnet.NOUN,'JJ':wordnet.ADJ,'VB':wordnet.VERB,'RB':wordnet.ADV}
listify = lambda item: item if type(item) == type([]) and item != None else list(item)

class SemanticWord(SemanticParser):

	def __init__(self,word,part_of_speech,db):
		self.part_of_speech = morphy_tag[part_of_speech] if part_of_speech in morphy_tag else wordnet.NOUN
		self.word = wordnet.morphy(word,self.part_of_speech) #Lemmatization

		self.synset = listify(wordnet.synsets(word,pos=self.part_of_speech)) if self.word else None
		self.orphan = not self.synset
		self.db = db
		self.lemmatizer = WordNetLemmatizer()
		self.kernel = {}

	def calculate_weight(self,synset, verbose=False,cutoff=0.2):

		prior = np.ones((len(synset),))/float(len(synset))

		weights = np.nan_to_num(np.array([np.average([freqs.freq(token) 
				for token in sense.lemma_names 
					if token not in stopwords 
					and synset[0].name.split('.')[0] not in token
					and sense.name.split('.')[0] not in token
					and '_' not in token]) 
						for sense in synset]))
		weights[weights==0]=1
		weights /= prior
		weights /= weights.sum()
		#Should update not replace information
		#Creating the semantic kernel is, itself a publication
		if verbose:
			print '*****%s****'%(synset)
			for weight,sense in zip(weights,synset):
				print 'Weight: %.02f as in %s, lemmas %s'%(weight,sense.definition, 
					' '.join([token for token in sense.lemma_names 
								if token not in stopwords 
								and synset[0].name.split('.')[0] not in token
								and sense.name.split('.')[0] not in token
								and '_' not in token]))
			print '*********'

		return weights
	def lookup(self,other):
		#construct query
		#for second pass use Google N-grams 
		#http://googleresearch.blogspot.com/2006/08/all-our-n-gram-are-belong-to-you.html
		#Way to visualize semantic kernels
		#Coverage will improve if using something better than Brown Corpus. Edinburgh Internet?
		query = '%s-%s'%(self.word,other.word)
		if query not in self.db:
			transpose_query = '%s-%s'%(other.word,self.word)
			if transpose_query in self.db:
				return self.db[transpose_query]
			else:
				similarity = np.empty((len(self.synset)*len(other.synset)))
				similarity[:] = np.nan

				a_kernel = np.array([sum([lemma.count() for lemma in a.lemmas()])
								for a in self.synset]).astype(float)

				a_kernel /= a_kernel.sum()

				b_kernel = np.array([sum([lemma.count() for lemma in a.lemmas()])
								for a in other.synset]).astype(float)

				b_kernel /= b_kernel.sum()
				

				for i,a in enumerate(self.synset):
					a_weight = sum([lemma.count() for lemma in a.lemmas()])
					for j,b in enumerate(other.synset):
							b_weight = sum([lemma.count() for lemma in b.lemmas()])
							similarity[i*len(other.synset)+j] = a.jcn_similarity(b,brown_ic)*a_kernel[i]*b_kernel[j]

				return 1-np.nanmedian(similarity)
		else:
			return self.db[query]

	def __sub__(self,other):
		if self.synset and other.synset: #Not orphans
			if set(self.synset) == set(other.synset): 
				return 0  #Two words have identical senses
			else:
				return self.lookup(other)
		else:
			return np.nan

	def __repr__(self):
		return 'word: %s \n sense: %s'%(self.word,pformat(self.synset) if not self.orphan else 'Not in WordNet')