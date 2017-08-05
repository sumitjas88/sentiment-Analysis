# -*- coding: utf-8 -*-
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

class HackAriba:
	def __init__(self):
		print "init of file"
		self.clf = LinearSVC()
		self.gnb = MultinomialNB()
		self.bigram_vectorizer = CountVectorizer(ngram_range=(2,2),token_pattern=r'\b\w+\b', min_df=1,lowercase=True)
		self.main_hack()
		print "end of file"
		sys.stdout.flush()

	# Punctuations
	# punctuations = \
	# 	[	\
	# 		('__PUNC_EXCL',		[',', ',', ] )	,\
	# 		('__PUNC_QUES',		[',', ',', ] )	,\
	# 		('__PUNC_ELLP',		['...', '.', ] )	,\
	# 		#FIXME : MORE? http://en.wikipedia.org/wiki/Punctuation
	# 	]

	def punctuations_repl(self,text):
		repl = []
		for (key, parr) in punctuations :
			for punc in parr :
				if punc in text:
					repl.append(key)
		if( len(repl)>0 ) :
			return ' '+' '.join(repl)+' '
		else :
			return ' '

	def pre_process_input_data(self,input_file_ptr):
		tweet_dict = {}
		input_file = pandas.read_csv(input_file_ptr,sep=",",usecols=(5,0))
		# print type(input_file).__name__
		return input_file

	def clean_data_to_feed_classifier(self,tweests):
		st = PorterStemmer()
		stop = stopwords.words('english')
		parsed_tweests = []
		for x in tweests:
			y=x[0]
			y = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",y).split())
			y = ' '.join(re.sub(r'(.)\1+', r'\1\1', i.lower())  for i in y.split() if i not in stop)
			y = ' '.join(st.stem(i) for i in y.split() if len(i) > 3 and i.isalpha() and wordnet.synsets(i))
			# y = punctuations_repl(y)
			print y
			parsed_tweests.append(y)
		return parsed_tweests
	def clean_data_to_feed_classifier_nt(self,tweests):
		st = PorterStemmer()
		stop = stopwords.words('english')
		parsed_tweests = []
		for x in tweests:
			y=x
			y = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",y).split())
			y = ' '.join(re.sub(r'(.)\1+', r'\1\1', i.lower())  for i in y.split() if i not in stop)
			y = ' '.join(st.stem(i) for i in y.split() if len(i) > 3 and i.isalpha() and wordnet.synsets(i))
			# y = punctuations_repl(y)
			print y
			parsed_tweests.append(y)
		return parsed_tweests

	def get_tweest_and_sentiments(self,tweests_dataframe):
		tweests_array =  tweests_dataframe.as_matrix(columns=tweests_dataframe.columns[1:])
		sentiments_array =  tweests_dataframe.as_matrix(columns=tweests_dataframe.columns[0:1])
		return tweests_array,sentiments_array

	def do_K_fold_cross_validation(self,classifier_svm,classifier_nb,data_set,class_set):
		kf = KFold(len(class_set), n_folds=10)
		print (type(data_set).__name__)
		print (type(class_set).__name__)
		print (data_set.shape)
		print (len(class_set))
		for train_index, test_index in kf:
			print (("TRAIN_INDEX %s and TEST_INDEX %s "%(train_index,test_index)))
			X_train, X_test = data_set[train_index], data_set[test_index]
			y_train, y_test = class_set[train_index], class_set[test_index]
			print (("data %s and class %s "%(X_train.shape,y_train.size)))
			# classifier_svm.fit(X_train,y_train)
			classifier_nb.fit(X_train,y_train)
			# y_predict = classifier_svm.predict(X_test)
			# print accuracy_score(y_test, y_predict)
			y_predict = classifier_nb.predict(X_test)
			print (accuracy_score(y_test,y_predict))
		return classifier_nb

	# Thinking to do 10-fold cross validation to improve the classifier accuracy but it will take longer time to train the
	# classifier.

	def main_hack(self):
		input_train_file_ptr = "trainingandtestdata/training.1600000.processed.noemoticon.csv"
		input_test_file_ptr = "trainingandtestdata/testdata.manual.2009.06.14.csv"
		# read the csv file and return the pandas dataframe with two column as tweets and sentiment as columns.
		train_tweests_with_sentiments = self.pre_process_input_data(input_train_file_ptr)
		test_tweets_data = self.pre_process_input_data(input_test_file_ptr)

		# print tweests_array
		tweets_array, sentiments_array = self.get_tweest_and_sentiments(train_tweests_with_sentiments)
		print(("size of tweets array is %s and sentiment array is %s  " % (tweets_array.size, sentiments_array.size)))
		test_tweets,test_sentiments = self.get_tweest_and_sentiments(test_tweets_data)
		test_sentiments =  test_sentiments.flatten()
		print(("size of test tweets array is %s and test sentiment array is %s  " % (test_tweets.size, test_sentiments.size)))
		parsed_train_tweets = self.clean_data_to_feed_classifier(tweets_array)
		parsed_test_tweets = self.clean_data_to_feed_classifier(test_tweets)
		# print parsed_tweests
		x = self.bigram_vectorizer.fit_transform(parsed_train_tweets)
		print (x.size)
		# print bigram_vectorizer.get_feature_names()
		self.bigram_vectorizer.build_analyzer()
		print ("done 1")
		# print bigram_vectorizer.get_feature_names()
		res = self.bigram_vectorizer.transform(parsed_test_tweets)
		print ("done 2")

		print ("done 2")
		trained_classifier = self.do_K_fold_cross_validation(self.clf,self.gnb,x,sentiments_array.flatten())
		# trained_classifier.fit(x, sentiments_array.flatten())
		print ("done 3")
		output =  trained_classifier.predict(res)
		# print output
		print (accuracy_score(test_sentiments,output))
	    # bigram_vectorizer.get_feature_names()
	    # analyze = bigram_vectorizer.build_analyzer()
	    # analyze



	# if __name__ == '__main__':
	#     main()
e = HackAriba()
