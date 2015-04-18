import string 

directory = json.load(open('directory.json',READ))		
stopwords = [word.rstrip('\r\n').strip() for word in open(directory['stopwords'],READ).readlines()]
emoticons = [word.rstrip('\r\n').strip() for word in open(directory['emoticons'],READ).readlines()]
punctuation = set(string.punctuation) 

READ = 'rb'
WRITE = 'wb'
class SemanticParser(object):
	def __init__(self):
		
