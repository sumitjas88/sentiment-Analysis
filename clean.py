import pandas
import numpy
import sys
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk import PorterStemmer
from sklearn.cross_validation import KFold
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB

class Clean:

	def __init__(self):
		print "cleaning"

	def clean_data_to_feed_classifier(self,tweests):
		st = PorterStemmer()
		stop = stopwords.words('english')
		parsed_tweests = []
		for x in tweests:
			y=x
			y = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",y).split())
			y = ' '.join(re.sub(r'(.)\1+', r'\1\1', i.lower())  for i in y.split() if i not in stop)
			y = ' '.join(st.stem(i) for i in y.split() if len(i) > 3 and i.isalpha() and wordnet.synsets(i))
			# y = punctuations_repl(y)
			#print y
			parsed_tweests.append(y)
		return parsed_tweests
