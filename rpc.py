import zerorpc
from hack_ariba import HackAriba

class HelloRPC(object):

	def __init__(self):
		self.classifier = HackAriba()
	def get_sentiment_of_list_of_tweets(self, list_of_tweets):
		list_of_text =[]
		for key, value in list_of_tweets.iteritems():
			list_of_text.append(value)
		print list_of_text
		clean_text = self.classifier.clean_data_to_feed_classifier_nt(list_of_text)
		print clean_text
		#text_vector = self.classifier.bigram_vectorizer.fit_transform(parsed_train_tweets)
		text_vector = self.classifier.bigram_vectorizer.transform(clean_text)
		predict = self.classifier.gnb.predict(text_vector)
		print predict
		count = 0
		for key in list_of_tweets.keys():
			list_of_tweets[key]=predict[count]
			count = count+1
		return list_of_tweets

s = zerorpc.Server(HelloRPC())
s.bind("tcp://0.0.0.0:4242")
s.run()
