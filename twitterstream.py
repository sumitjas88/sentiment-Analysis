import oauth2 as oauth
import urllib2 as urllib
import sys
import json
from TwitterData import TwitterDataObject
import unicodedata

# See assignment1.html instructions or README for how to get these credentials

class TwitterStream:





    def __init__(self):
      self.api_key = "kdyDA6M0f2W0pK0Kwqy60fYTF"
      self.api_secret = "vp27gUhGD3m2uv0NmlZrcwP6o8QqgGZMbJaud7iZCEHUY9ByyE"
      self.access_token_key = "2599282818-nyiJbM3bskcxiWREiyhP7UwfBVBcbBwcHIVjvO5"
      self.access_token_secret = "om6xk1CUIC4LoIkE62dd7k4ioWr7lfQiiOfZC3YhOeQmv"

      self._debug = 0

      self.oauth_token    = oauth.Token(key=self.access_token_key, secret=self.access_token_secret)
      self.oauth_consumer = oauth.Consumer(key=self.api_key, secret=self.api_secret)

      self.signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

      self.http_method = "GET"


      self.http_handler  = urllib.HTTPHandler(debuglevel=self._debug)
      self.https_handler = urllib.HTTPSHandler(debuglevel=self._debug)

    def twitterreq(self,url, method, parameters):
      req = oauth.Request.from_consumer_and_token(self.oauth_consumer,
                                                 token=self.oauth_token,
                                                 http_method=self.http_method,
                                                 http_url=url,
                                                 parameters=parameters)

      req.sign_request(self.signature_method_hmac_sha1, self.oauth_consumer, self.oauth_token)

      headers = req.to_header()

      if self.http_method == "POST":
        encoded_post_data = req.to_postdata()
      else:
        encoded_post_data = None
        url = req.to_url()

      opener = urllib.OpenerDirector()
      opener.add_handler(self.http_handler)
      opener.add_handler(self.https_handler)

      response = opener.open(url, encoded_post_data)

      return response

    def fetchSample(self,query):
    # query = sys.argv[1]
      url = "https://stream.twitter.com/1/statuses/sample.json"
      url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=" + query
      url = "https://api.twitter.com/1.1/search/tweets.json?q=%23 " + query + "&count=100" + "&lang=en"
      parameters = []
      response = self.twitterreq(url, "GET", parameters)
      result =[]
      for line in response:
        tweets = json.loads(line)
        for tweet_json in tweets["statuses"]:
          if "text" in tweet_json.keys():
            # if "lang" in tweet_json.keys() and tweet_json["lang"] == "en":
              text = unicodedata.normalize('NFKD', tweet_json["text"]).encode('ascii','ignore')
             # print text
              created_at = tweet_json["created_at"]
              user = "no user"
              if "name" in tweet_json["user"].keys():
                user = tweet_json["user"]["name"]
              twitt_location = "not found"
              if "location" in tweet_json["user"].keys():
                twitt_location = tweet_json["user"]["location"]
              twitt_id = tweet_json["id"]
             # print 'amit',text,twitt_id,-1,twitt_location,created_at
              twittObj = TwitterDataObject(text,twitt_id,-1,twitt_location,created_at)
              result.append(twittObj)
      return result

# if __name__ == '__main__':
#   print "let me test"
#   print fetchsamples()
