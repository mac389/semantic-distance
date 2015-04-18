import itertools,string,re,json

import SemanticWord as sw
import numpy as np

from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet
from pprint import pprint
from termcolor import colored

CONTRACTIONS2 = [re.compile(r"(?i)(.)('ll|'re|'ve|n't|'s|'m|'d)\b"),
                 re.compile(r"(?i)\b(can)(not)\b"),
                 re.compile(r"(?i)\b(D)('ye)\b"),
                 re.compile(r"(?i)\b(Gim)(me)\b"),
                 re.compile(r"(?i)\b(Gon)(na)\b"),
                 re.compile(r"(?i)\b(Got)(ta)\b"),
                 re.compile(r"(?i)\b(Lem)(me)\b"),
                 re.compile(r"(?i)\b(Mor)('n)\b"),
                 re.compile(r"(?i)\b(T)(is)\b"),
                 re.compile(r"(?i)\b(T)(was)\b"),
                 re.compile(r"(?i)\b(Wan)(na)\b")]
CONTRACTIONS3 = [re.compile(r"(?i)\b(Whad)(dd)(ya)\b"),
                 re.compile(r"(?i)\b(Wha)(t)(cha)\b")]

READ = 'rb'

directory = json.load(open('directory.json',READ))		

stopwords = [word.rstrip('\r\n').strip() for word in open(directory['stopwords'],READ).readlines()]
emoticons = [word.rstrip('\r\n').strip() for word in open(directory['emoticons'],READ).readlines()]
punctuation = set(string.punctuation) 

class SemanticString(object):
	def __init__(self, text,db):
		self.text = text
		self.db=db

		self.tokens = [sw.SemanticWord(token,part_of_speech,self.db) 
						for token,part_of_speech in self.pos_tag(self.word_tokenize(text))
						if token not in punctuation and token not in stopwords]		
		self.tokens = filter(lambda token: not token.orphan,self.tokens)

		self.synsets = [token.synset for token in self.tokens]
	def __len__(self):
		return len(filter(None,self.synsets)) if len(filter(None,self.synsets)) > 0 else None

	def word_tokenize(self,text):
		for regexp in CONTRACTIONS2:
			text = regexp.sub(r'\1 \2', text)
		for regexp in CONTRACTIONS3:
			text = regexp.sub(r'\1 \2 \3', text)

		# Separate most punctuation
		#text = re.sub(r"([^\w\.\'\-\/,&])", r' \1 ', text)

		# Separate commas if they're followed by space.
		# (E.g., don't separate 2,500)
		text = re.sub(r"(,\s)", r' \1', text)

		# Separate single quotes if they're followed by a space.
		text = re.sub(r"('\s)", r' \1', text)

		# Separate periods that come before newline or end of string.
		text = re.sub('\. *(\n|$)', ' . ', text)

		return text.split()

	def pos_tag(self,text):
		return [(word,'EMO') if word in emoticons else (word,tag) for word,tag in pos_tag(text)]

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