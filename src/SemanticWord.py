import itertools
import string
import json

import numpy as np

from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import FreqDist

from pprint import pformat
from termcolor import colored



morphy_tag = {'NN':wordnet.NOUN,'JJ':wordnet.ADJ,'VB':wordnet.VERB,'RB':wordnet.ADV}
listify = lambda item: item if type(item) == type([]) and item != None else list(item)
READ = 'rb'
directory = json.load(open('/Volumes/My Book/Toxic/dictionary.json',READ))

stopwords = [word.rstrip('\r\n').strip() for word in open(directory['stopwords'],READ).readlines()]
emoticons = [word.rstrip('\r\n').strip() for word in open(directory['emoticons'],READ).readlines()]
punctuation = set(string.punctuation) #Can make more efficient with a translator table
corpus = [word.rstrip('\r\n').strip().split() for word in open(directory['corpus'],READ).readlines()][0]
freqs = FreqDist(corpus)
class SemanticWord(object):

	def __init__(self,word,part_of_speech,lookuptable):
		self.part_of_speech = morphy_tag[part_of_speech] if part_of_speech in morphy_tag else wordnet.NOUN
		self.word = wordnet.morphy(word,self.part_of_speech) #Lemmatization

		self.synset = listify(wordnet.synsets(word,pos=self.part_of_speech)) if self.word else None
		self.orphan = not self.synset
		self.db = lookuptable
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
		query = '%s-%s'%(self.word,other.word)
		if query not in self.db:
			transpose_query = '%s-%s'%(other.word,self.word)
			if transpose_query in self.db:
				self.db[query] = self.db[transpose_query]
			else:
				distance = np.zeros((len(self.synset)*len(other.synset)))
				#one_kernel = self.calculate_weight(self.synset)
				#two_kernel = self.calculate_weight(other.synset)

				for i,a in enumerate(self.synset):
					for j,b in enumerate(other.synset):
						val = min(a.path_similarity(b),b.path_similarity(a))
						#val *= one_kernel[i] * two_kernel[j]
						distance[i*len(other.synset)+j] = val
				distance = np.average(distance)
				self.db[query] = distance 
		return self.db[query]

	def __sub__(self,other):
		if self.synset and other.synset and self.part_of_speech == other.part_of_speech: 
			return 0 if self.word == other.word else self.lookup(other)
		else:
			return np.nan

	def __repr__(self):
		return 'word: %s \n sense: %s'%(self.word,pformat(self.synset) if not self.orphan else 'Not in WordNet')