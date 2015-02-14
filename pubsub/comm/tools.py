'''
Created on Feb 11, 2015

@author: ronaldjosephdesmarais
'''

class SubscriberMessageQueue(object):
    
    def __init__(self,maxsize):
        self.maxsize=maxsize
        self.queue = []
    
    def retrieve(self):
        print "Try to Reteive Message"
        try:
            return self.queue.pop()
        except:
            return None
    
    def send(self,msg):
        if len(self.queue) < self.maxsize:
            self.queue.append(msg)
            return True
        else:
            return False
        
class MessageQueue(object):
    
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
            print "Sending Message %s to %s"%(msg,sub)
            sub.send(msg)