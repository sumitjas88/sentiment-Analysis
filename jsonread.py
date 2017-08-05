import sys;
from  twitterstream import TwitterStream;
import zerorpc
import json

twitterObj = TwitterStream()
list_of_twittObj = twitterObj.fetchSample(sys.argv[1])
c = zerorpc.Client()
c.connect("tcp://127.0.0.1:4242")
dict_of_id_and_text = {}
dict_of_id_and_twittObj = {}
for t in list_of_twittObj:
	dict_of_id_and_text[t.twitt_id] = t.text
	dict_of_id_and_twittObj[t.twitt_id] = t
# print dict_of_id_and_text
twee_id_with_sentiment = c.get_sentiment_of_list_of_tweets(dict_of_id_and_text)
# print twee_id_with_sentiment
output = []
# print (type(twee_id_with_sentiment).__name__)
for key,value in twee_id_with_sentiment.iteritems():
	twittObj = dict_of_id_and_twittObj.get(key)
	twittObj.set_sentiment(value)
	output.append(twittObj)
print json.dumps(output, default=lambda o: o.__dict__)
#print list_of_twittObj[0].text

# hack = HackAriba()
# print "hackariba called"
sys.stdout.flush()
