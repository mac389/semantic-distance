import re

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