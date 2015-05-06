import itertools,string,re,json

import SemanticWord as sw
import numpy as np
import utils as tech

from nltk.corpus import wordnet
from termcolor import colored
from SemanticParser import SemanticParser

class SemanticString(SemanticParser):
	def __init__(self, text,db,inspect=False):
		self.text = text
		self.db=db
		self.inspect = inspect

		self.tokens = [sw.SemanticWord(token,part_of_speech,self.db,inspect=self.inspect) for token,part_of_speech in text]		
		self.tokens = filter(lambda token: not token.orphan,self.tokens)
		self.synsets = [token.synset for token in self.tokens]

	def __len__(self):
		return len(filter(None,self.synsets)) if len(filter(None,self.synsets)) > 0 else None

	def __sub__(self,other):
		if self.text == other.text:
			return 0
		else:
			distances = np.array([self.tokens[i] - other.tokens[j] 
								for i in xrange(len(self.tokens)) 
								for j in xrange(len(other.tokens))])


			distances = distances[~np.isnan(distances)]
		return np.average(distances) if len(distances)>0 else np.nan

	def __repr__(self):
		return  '%s--> %s'%(colored(self.text,'red'),colored(' '.join(filter(None,[token.word for token in self.tokens])),'green'))