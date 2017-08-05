import zerorpc
from hack_ariba import HackAriba
from clean import Clean

class HelloRPC(object):

	def __init__(self):
		# self.classifier = HackAriba()
		self.clean = Clean()
	def get_sentiment_of_list_of_tweets(self, list_of_tweets):
		list_of_text =[]
		for key, value in list_of_tweets.iteritems():
			list_of_text.append(value)
		print list_of_text
		clean_text = self.clean.clean_data_to_feed_classifier(list_of_text)
		print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
		print clean_text
		print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
		return clean_text
		#text_vector = self.classifier.bigram_vectorizer.fit_transform(parsed_train_tweets)
		# text_vector = self.classifier.bigram_vectorizer.fit_transform(clean_text)
		# return self.classifier.gnb.predict(text_vector)

s = zerorpc.Server(HelloRPC())
s.bind("tcp://0.0.0.0:4290")
s.run()
