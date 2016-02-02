from twisted.web import server
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor, task
import json
import time
import dbFns.main as db
import copy

class Publisher():
    def __init__(self):
        pass

    def handlePublishRequest(self,request,formatResponse):
        args = request.args
        message="default" 
        channel="default"  
        if 'message' in args:
            message =  args['message'][0]

        if 'channel' in args:
            channel =  args['channel'][0]

        username = args['username'][0]

        if (db.addMessage(channel,username,int(time.time()),message)):
            return message,channel,formatResponse(request, 1, {'messages':'success'})
        else:
            return message,channel,formatResponse(request, 0, {'messages':'failure'})

        

    def AddChannel(self,request,formatResponse):
        args = request.args
        if 'username' in args and 'channel' in args:
            if (db.addPubChannel(args['username'][0],args['channel'][0])):
                return formatResponse(request, 1, {'messages':'success'})
            else:
                return formatResponse(request, 0, {'messages':'failure'})
        else:
            return formatResponse(request, 0, {'message':'failed'})


    def RemoveChannel(self,request,formatResponse):
        args = request.args
        if 'username' in args and 'channel' in args:
            if (db.removePubChannel(args['username'][0],args['channel'][0])):
                return formatResponse(request, 1, {'messages':'success'})
            else:
                return formatResponse(request, 0, {'messages':'failure'})
        else:
            return formatResponse(request, 0, {'message':'failed'})


    def ChangeEmail(self,request,formatResponse):
        args= request.args
        if 'username' in args and 'email' in args:
            if (db.changePubEmail(args['username'][0],args['email'][0])):
                data = {'messages':'success'}
                return formatResponse(request, 1,data)
            else:
                data = {'messages':'failure'}
                return formatResponse(request, 0,data)
        else:
            return formatResponse(request, 0, {'message':'failed'})

    def channelList(self,request,formatResponse):
        args= request.args
        if 'username' in args :
            data = {'channels':db.getPubChannelList(args['username'][0])}
            return formatResponse(request, 1,data)
        else:
            return formatResponse(request, 0, {'message':'failed'}),None,None



class Subscriber():
    def __init__(self):
        pass


    def SubscribeChannel(self,request,formatResponse):
        args = request.args
        if 'username' in args and 'channel' in args:
            if (db.addSubChannel(args['username'][0],args['channel'][0])):
                data = {'messages':'success'}
                return formatResponse(request, 1,data),args['channel'][0]
            else:
                data = {'messages':'failure'}
                return formatResponse(request, 0,data),args['channel'][0]
        else:
            return formatResponse(request, 0, {'message':'failed'}),None

    def UnSubscribeChannel(self,request,formatResponse):
        args = request.args
        if 'username' in args and 'channel' in args:
            if (db.removeSubChannel(args['username'][0],args['channel'][0])):
                data = {'messages':'success'}
                return formatResponse(request, 1,data),args['channel'][0]
            else:
                data = {'messages':'failure'}
                return formatResponse(request, 0,data),args['channel'][0]
        else:
            return formatResponse(request, 0, {'message':'failed'}),None


    def ChangeEmail(self,request,formatResponse):
        args= request.args
        if 'username' in args and 'email' in args:

            if (db.changeSubEmail(args['username'][0],args['email'][0])):
                data = {'messages':'success'}
                return formatResponse(request, 1,data),args['username'][0],args['email'][0]
            else:
                data = {'messages':'failure'}
                return formatResponse(request, 0,data),args['username'][0],args['email'][0]
        else:
            return formatResponse(request, 0, {'message':'failed'}),None,None

    def channelList(self,request,formatResponse):
        args= request.args
        if 'username' in args :
            data = {'channels':db.getSubChannelList(args['username'][0])}
            return formatResponse(request, 1,data)
        else:
            return formatResponse(request, 0, {'message':'failed'}),None,None

    def getHistory(self,request,formatResponse):
        args= request.args
        if 'username' in args :
            data = {'history':db.getHistory(args['username'][0])}
            return formatResponse(request, 1,data)
        else:
            return formatResponse(request, 0, {'message':'failed'})

    def handleSubscribeRequest(self,request,formatResponse):
        # return this for return atleast once policy from the database
        
        args = request.args
        response=server.NOT_DONE_YET
        userId=-1 

        if 'user' in args:
            userId=args['user'][0]
        print "Getting Message for user",userId

        messages=db.getMessages(userId,db.getLastTimestamp(userId))


        if len(messages) > 0:
            response=formatResponse(request, 1, {'messages':messages})
   
        return userId,response

    def filterSubscriber(self,channel,userId):
        return db.isSubscribed(userId,channel)
       




class ServiceHandler(Resource):
    isLeaf = True
    def __init__(self):
        self.subscribersList=[]
        self.subscriberUserId=dict()
        self.publisher=Publisher()
        self.subscriber=Subscriber()
        Resource.__init__(self)

    def render(self, request):
        """
        Handle a new request
        """
        print request.path
        request.setHeader('Content-Type', 'application/json')
        args = request.args
           
        # set jsonp callback handler name if it exists
        if 'callback' in args:
            request.jsonpcallback =  args['callback'][0]
        
        # set lastupdate if it exists
        if 'lastupdate' in args:
            request.lastupdate =  args['lastupdate'][0]
        else:
            request.lastupdate = 0

        return self.urlRequestHandler(request)


        
    def urlRequestHandler(self,request):
        if request.path == "/pub":
            message,channel,response=self.publisher.handlePublishRequest(request,self.__format_response)
            reactor.callLater(0.001, self.processDelayedRequests,channel)
            return response

        elif request.path == "/sub":
            userId,response= self.subscriber.handleSubscribeRequest(request,self.__format_response)
            if response==server.NOT_DONE_YET:
                self.subscribersList.append(request)
                self.subscriberUserId[request]=userId
                print len(self.subscribersList)
                print "Saving the request",userId
            else:
                db.updateTimestamp(userId,int(time.time()))
                print "Sending the request",userId

            
            # print "Updating Timestamp",db.updateTimestamp(userId,int(time.time()))
            return response   

        elif request.path=="/pubAddChannel":
            response=self.publisher.AddChannel(request,self.__format_response)
            return response

        elif request.path=="/pubRemoveChannel":
            response=self.publisher.RemoveChannel(request,self.__format_response)
            return response

        elif request.path=="/changePubEmail":
            response=self.publisher.ChangeEmail(request,self.__format_response)
            return response

        elif request.path=="/subChannel":
            response,channel=self.subscriber.SubscribeChannel(request,self.__format_response)
            return response

        elif request.path=="/unsubChannel":
            response,channel=self.subscriber.UnSubscribeChannel(request,self.__format_response)
            return response

        elif request.path=="/changeSubEmail":
            response,oldEmail,newEmail=self.subscriber.ChangeEmail(request,self.__format_response)
            #  only if response was success
            reactor.callLater(0.001, self.handleEmailChange,oldEmail,newEmail)
            return response

        elif request.path=="/pubChannelList":
            response=self.publisher.channelList(request,self.__format_response)
            return response

        elif request.path=="/subChannelList":
            response=self.subscriber.channelList(request,self.__format_response)
            return response
        elif request.path=="/getHistory":
            response=self.subscriber.getHistory(request,self.__format_response)
            return response


    def handleEmailChange(self,oldEmail,newEmail):
        for request in self.subscribersList:
            if (self.subscriberUserId[request]==oldEmail):    
                response=self.__format_response(request, 0, {'messages':[]})
                try:
                    request.write(response)
                    request.finish()
                    db.updateTimestamp(newEmail,int(time.time())) 
                except:
                    # Connection was lost
                    print 'connection lost before complete.'
                finally:
                    # Remove request from list
                    self.subscribersList.remove(request)
                    self.subscriberUserId.pop(request, None)

    def processDelayedRequests(self,channel):
        """
        Processes the delayed requests that did not have
        any data to return last time around.
        """    
        # run through delayed requests
        print "Number of pending Requests:",len(self.subscribersList)

        for iterVal in xrange(len(self.subscribersList) - 1, -1, -1):
            request=self.subscribersList[iterVal]
            # attempt to get data again
            print "[processDelayedRequests]Current Request:",channel,self.subscriberUserId[request]

            if not self.subscriber.filterSubscriber(channel,self.subscriberUserId[request]):
                # db.updateTimestamp(self.subscriberUserId[request],int(time.time()))
                continue

            print "[processDelayedRequests]Sending Data ",channel,self.subscriberUserId[request]

            userId,response = self.subscriber.handleSubscribeRequest(request,self.__format_response)
            

            # write response and remove request from list if data is found
            print "writing response"
            print response
            # if not response==server.NOT_DONE_YET :
            try:
                request.write(response)
                request.finish()
                db.updateTimestamp(self.subscriberUserId[request],int(time.time()))
            except:
                # Connection was lost
                print 'connection lost before complete.'
            finally:
                # Remove request from list
                self.subscribersList.remove(request)
                self.subscriberUserId.pop(request, None)


    def __format_response(self, request, status, data):
        """
        Format responses uniformly
        """
        # Set the response in a json format
        response = json.dumps({'status':status,'timestamp': int(time.time()), 'data':data})

        # Format with callback format if this was a jsonp request
        if hasattr(request, 'jsonpcallback'):
            return request.jsonpcallback+'('+response+')'
        else:
            return response
############################################# 

if __name__ == '__main__':
    resource = ServiceHandler()
    resource.putChild('pub', ServiceHandler())
    resource.putChild('sub', ServiceHandler())
    factory = Site(resource)
    reactor.listenTCP(8000, factory)
    reactor.run()
se