from django.db import models
from djangotoolbox.fields import ListField,DictField
from datetime import datetime
from django.db.models.signals import post_save

class channels(models.Model):
	channelName=models.TextField()   # name of the channel, the channel is unique
	messages = ListField(DictField()) # stores the message text, timestamp, and publisher name 

	def to_json(self):
		return {"_id":self.id,
			"channelName":self.channelName,
			"messages" : self.messages,
			}

	class Meta:
		db_table = 'channels'


class publishers(models.Model):
	publisherName =models.TextField()
	channelList= ListField()
	
	def to_json(self):
		return {"_id":self.id,
			"publisherName" : self.publisherName,
			"channelList" : self.channelList,
			}

	class Meta:
		db_table = 'publishers'

class subscribers(models.Model):
	subscriberName =models.TextField()
	channelList= ListField()
	lastTimestamp= models.IntegerField()
	
	def to_json(self):
		return {"_id":self.id,
			"subscriberName" : self.subscriberName,
			"channelList" : self.channelList,
			"lastTimestamp" : self.lastTimestamp
			}

	class Meta:
		db_table = 'subscribers'





