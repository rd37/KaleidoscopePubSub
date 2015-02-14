from django.db import models
    
class service_call(models.Model):
    address = models.URLField(max_length=200)
    port = models.IntegerField()
    service = models.CharField(max_length=200)
    
    def __str__(self):
        return "%s:%s/%s"%(self.address)

class message_queue(models.Model):
    msgkey = models.CharField(max_length=200)
    
    def __str__(self):
        return "%s"%(self.msgkey)
        
class websocket_call(models.Model):
    webkey = models.CharField(max_length=200)
    
    def __str__(self):
        return "%s"%(self.webkey)
    
class subscribers(models.Model):
    method = models.CharField(max_length=200) #either service_call or websocket_call
    #method_key = models.IntegerField()
    method_key = models.CharField(max_length=200)
    
    def retrieve(self,j_obj,msg_queues):
        #print "Try to retrieve Message using Msg Queue %s using %s"%(msg_queues,self.method_key)
        if j_obj["method"] == "SubscriberMessageQueue":
            #print "Use key %s to Get Queue from %s"%(self.method_key,msg_queues)
            q = msg_queues["%s"%self.method_key]
            return q.retrieve()
    
    def __str__(self):
        return "%s-%s"%(self.method,self.method_key)

class publishers(models.Model):
    method = models.CharField(max_length=200) #either service_call or websocket_call
    #method_key = models.IntegerField()
    method_key = models.CharField(max_length=200)
    
    def send(self,j_obj,msg_queues):
        #print "Try to send Message using Msg Queue %s using %s"%(msg_queues,self.method_key)
        if j_obj["method"] == "MessageQueue":
            q = msg_queues["%s"%self.method_key]
            q.send(j_obj["msg"])
        
    def __str__(self):
        return "%s-%s"%(self.method,self.method_key)
    
class subscriptions(models.Model):
    pubs = models.ForeignKey(publishers)
    subs = models.ForeignKey(subscribers)
    
    def __str__(self):
        return "%s-%s"%(self.pubs,self.subs)
    
    
    