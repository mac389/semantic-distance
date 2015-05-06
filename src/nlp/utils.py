import re,itertools

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

def format__1(digits,num):
	if digits<len(str(num)):
		raise Exception("digits<len(str(num))")
	return ' '*(digits-len(str(num))) + str(num)
	
def printmat(arr,row_labels=[], col_labels=[]): #print a 2d numpy array (maybe) or nested list
	max_chars = max([len(str(item)) for item in list(itertools.chain.from_iterable(arr))+col_labels]) #the maximum number of chars required to display any item in list
	if row_labels==[] and col_labels==[]:
		for row in arr:
			print '[%s]' %(' '.join(format__1(max_chars,i) for i in row))
	elif row_labels!=[] and col_labels!=[]:
		rw = max([len(str(item)) for item in row_labels]) #max char width of row__labels
		print '%s %s' % (' '*(rw+1), ' '.join(format__1(max_chars,i) for i in col_labels))
		for row_label, row in zip(row_labels, arr):
			print '%s [%s]' % (format__1(rw,row_label), ' '.join(format__1(max_chars,i) for i in row))
	else:
		raise Exception("This case is not implemented...either both row_labels and col_labels must be given or neither.")

def print_semantic_kernel(arr,row_labels=[],col_labels=[],row_kernel=[],col_kernel=[]):
	if row_kernel == [] and col_kernel == []:
		printmat(arr,row_labels=row_labels,col_labels=col_labels)
	else:
		max_chars = max([len(str(item)) for item in list(itertools.chain.from_iterable(arr))+col_labels]) #the maximum number of chars required to display any item in list
		if row_labels==[] and col_labels==[]:
			for row in arr:
				print '[%s]' %(' '.join(format__1(max_chars,i) for i in row))
		elif row_labels!=[] and col_labels!=[]:
			rw = max([len(str(item)) for item in row_labels]+[len(str(item)) for item in row_kernel]) #max char width of row__labels
			print '%s %s' % (' '*(2*rw+1), ' '.join(format__1(max_chars,i) for i in col_labels))
			print '%s %s' % (' '*(2*rw+1), ' '.join(format__1(max_chars,i) for i in col_kernel))
			for row_label, kernel, row in zip(row_labels, row_kernel, arr):
				print '%s (%s) [%s]' % (format__1(rw,row_label), format__1(rw,kernel),' '.join(format__1(max_chars,i) for i in row))
		else:
			raise Exception("This case is not implemented...either both row_labels and col_labels must be given or neither.")

def word_tokenize(text):
	#Fails if no space between emoticon and word
	
	for regexp in CONTRACTIONS2:
		text = regexp.sub(r'\1 \2', text)
	for regexp in CONTRACTIONS3:
		text = regexp.sub(r'\1 \2 \3', text)

	# Separate most punctuation
	text = re.sub(r"([^\w\.\'\-\/,&])", r' \1 ', text)

	# Separate commas if they're followed by space.
	# (E.g., don't separate 2,500)
	text = re.sub(r"(,\s)", r' \1', text)

	# Separate single quotes if they're followed by a space.
	text = re.sub(r"('\s)", r' \1', text)

	# Separate periods that come before newline or end of string.
	text = re.sub('\. *(\n|$)', ' . ', text)

	return text.split()