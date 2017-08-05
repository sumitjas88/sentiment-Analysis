class TwitterDataObject:
	# text
	# twitt_id
	# sentiment
	# location
	# created_at

	def __init__(self, text,twitt_id,sentiment,location,created_at):
		self.text = text
		self.twitt_id = twitt_id
		self.sentiment = sentiment
		self.location = location
		self.created_at = created_at

	def set_sentiment(self,senti):
		self.sentiment = senti
