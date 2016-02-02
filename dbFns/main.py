# Django specific settings
import os
import json,yaml
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
from db.models import *

def changePubEmail(name,newName):
	addPublisher(name)
	try:
		publishers.objects.get(publisherName=newName)
		return False
	except:
		pass

	pubData=publishers.objects.get(publisherName=name)
	pubData.publisherName=newName
	pubData.save()
	print "[Change Publisher Email]",name,newName
	return True

def changeSubEmail(name,newName):
	addSubscriber(name)
	
	try:
		subscribers.objects.get(subscriberName=newName)
		return False
	except:
		pass	

	subData=subscribers.objects.get(subscriberName=name)
	subData.subscriberName=newName
	subData.save()
	print "[Change Subscriber Email]",name,newName
	return True

def addPublisher(name):
	try:
		publishers.objects.get(publisherName=name)
		return False
	except:
		pub=publishers(publisherName=name)
		pub.save()
		return True


def addChannel(name):
	try:
		channels.objects.get(channelName=name)
		return False
	except:
		ch=channels(channelName=name,messages=[])
		ch.save()
		return True


def addSubscriber(name):
	try:
		subscribers.objects.get(subscriberName=name)
		return False
	except:
		sub=subscribers(subscriberName=name,lastTimestamp=0)
		sub.save()
		return True


def addMessage(channel,publisher,timestamp,message):
	addPublisher(publisher)
	# addChannel(channel)

	data=dict()
	data['timestamp']=timestamp
	data['message']=message

	pubData=publishers.objects.get(publisherName=publisher)
	if not channel in pubData.channelList:
		return False
	data['publisher']=pubData.id
	channelData=channels.objects.get(channelName=channel)
	channelData.messages.append(data)
	channelData.save()
	print "[Publishing Message]",publisher,channel
	return True


def getMessages(subscriber,timestamp):
	addSubscriber(subscriber)
	subData=subscribers.objects.get(subscriberName=subscriber)
	result=list()
	for channel in subData.channelList:
		channelData=channels.objects.get(channelName=channel)
		l=channelData.messages
		for i in range(len(l)-1,-1,-1):
			if l[i]['timestamp'] > timestamp:
				pubData=publishers.objects.get(id=l[i]['publisher'])
				l[i]['publisher']=pubData.publisherName
				l[i]['channel']=channel
				result.append(l[i])
			else:
				continue
	return result

def isSubscribed(subscriber,channel):
	addSubscriber(subscriber)
	subData=subscribers.objects.get(subscriberName=subscriber)
	if channel in subData.channelList:
		return True
	else:
		return False


def addPubChannel(name,channel):
	addPublisher(name)
	addChannel(channel)
	pubData=publishers.objects.get(publisherName=name)
	if not channel in pubData.channelList:
		pubData.channelList.append(channel)
		pubData.save()
		print "[Adding Channel] ",name,channel
		return True
	else:
		return False


def removePubChannel(name,channel):
	addPublisher(name)
	pubData=publishers.objects.get(publisherName=name)
	if channel in pubData.channelList:
		pubData.channelList.remove(channel)
		pubData.save()
		print "[Removing Channel] ",name,channel
		return True
	else:
		return False


def getLastTimestamp(subscriber):
	addSubscriber(subscriber)
	subData=subscribers.objects.get(subscriberName=subscriber)
	return subData.lastTimestamp

def getSubChannelList(subscriber):
	addSubscriber(subscriber)
	subData=subscribers.objects.get(subscriberName=subscriber)
	return subData.channelList

def getPubChannelList(publisher):
	addPublisher(publisher)
	pubData=publishers.objects.get(publisherName=publisher)
	return pubData.channelList

def getHistory(subscriber):
	addSubscriber(subscriber)
	subData=subscribers.objects.get(subscriberName=subscriber)
	result=list()
	for channel in subData.channelList:
		channelData=channels.objects.get(channelName=channel)
		l=channelData.messages
		for i in range(len(l)-1,-1,-1):
			l[i]['channel']=channel
			pubData=publishers.objects.get(id=l[i]['publisher'])
			l[i]['publisher']=pubData.publisherName
			result.append(l[i])
	return result


def updateTimestamp(subscriber,timestamp):
	addSubscriber(subscriber)
	subData=subscribers.objects.get(subscriberName=subscriber)
	subData.lastTimestamp=timestamp
	subData.save()
	return True




def addSubChannel(name,channel):
	addSubscriber(name)
	try:
		channels.objects.get(channelName=channel)
	except:
		return False

	subData=subscribers.objects.get(subscriberName=name)
	if not channel in subData.channelList:
		subData.channelList.append(channel)
		subData.save()
		print "[Adding Channel] ",name,channel
		return True
	else:
		return False


def removeSubChannel(name,channel):
	addSubscriber(name)
	subData=subscribers.objects.get(subscriberName=name)
	if channel in subData.channelList:
		subData.channelList.remove(channel)
		subData.save()
		print "[Removing Channel] ",name,channel
		return True
	else:
		return False



if __name__ == '__main__':
	print addPublisher('siddhant')
	print addSubscriber('siddhant')
	print addPublisher('siddhant')
	print addSubscriber('siddhant')
	print changePubEmail('siddhant','manocha')
	print changeSubEmail('siddhant','manocha')
	print changeSubEmail('siddhant','manocha')

	print addPubChannel('manocha','channel1')
	print addSubChannel('manocha','channel2')


	print addPubChannel('manocha','channel1')
	print addSubChannel('siddhant','channel1')

	print addMessage('channel1','manocha',10,"Hello world1")
	print addMessage('channel1','manocha',12,"Hello world2")

	print getMessages('siddhant',9)

	print isSubscribed('manocha','channel1')
	print isSubscribed('manocha','channel2')














