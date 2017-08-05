import pandas
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
stop = stopwords.words('english')
colnames = ['label', 'id', 'date','query', 'user', 'tweet']
data = pandas.read_csv('testdata.csv', names=colnames)
tweets = data.tweet.tolist()
refined  = []
for tweet in tweets:
	tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tweet).split())
	text = [i for i in tweet.split() if i not in stop]
#	print (tweet)
	str = ' '.join(text)
	refined.append(str)
print (refined)	
vectorizer = CountVectorizer(min_df=1)
X = vectorizer.fit_transform(refined)	
print (X.toarray())
