import string 

class SemanticParser(object):
	def __init__(self):
		self.directory = json.load(open('directory.json',READ))		
		self.stopwords = [word.rstrip('\r\n').strip() for word in open(directory['stopwords'],READ).readlines()]
		self.emoticons = [word.rstrip('\r\n').strip() for word in open(directory['emoticons'],READ).readlines()]
		self.punctuation = set(string.punctuation) 

		self.READ = 'rb'
		self.WRITE = 'wb'
