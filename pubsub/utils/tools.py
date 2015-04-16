'''
Created on Feb 11, 2015

@author: ronaldjosephdesmarais
'''

from websockets.api.ws_api import PubSub_WS_API
#Subscriber queue for polling
import thread

class WSSubscriberMessageQueue(object):
    
    def __init__(self,sub_ws_id):
        self.sub_ws_id=sub_ws_id
        #self.queue = []
    
    def send(self,msg):
        thread.start_new_thread(self.invoke, (msg,))
        
    def invoke(self,msg):
        #print "WS Try to send WS message %s to %s "%(msg,self.sub_ws_id)
        ws_api = PubSub_WS_API(None)
        ws_api.pushSubscriberMessage(msg.encode("ascii"),self.sub_ws_id)
        ws_api.closeConnection()

#Subscriber queue for polling
class SubscriberMessageQueue(object):
    
    def __init__(self,maxsize):
        self.maxsize=maxsize
        self.queue = []
    
    def retrieve(self):
        try:
            #print "Retrieving Message"
            return self.queue.pop()
        except Exception as e:
            #print "Subscriber Exception error %s"%e
            return None
    
    def send(self,msg):
        if len(self.queue) < self.maxsize:
            #print "appending message %s"%msg
            self.queue.append(msg)
            return True
        else:
            return False

#publisher creates this message queue for polling
class PublisherMessageQueue(object):
    
    def __init__(self,maxsize):
        self.maxsize=maxsize
        self.queue = []
        
    def subscribe(self,subscriber):
        if len(self.queue) > self.maxsize:
            return False
        else:
            self.queue.append(subscriber)
            return True
    
    def unsubscribe(self,subscriber):
        self.queue.remove(subscriber)
        
    def send(self,msg):
        for sub in self.queue:
            #print "Sending Message %s to %s"%(msg,sub)
            sub.send(msg)