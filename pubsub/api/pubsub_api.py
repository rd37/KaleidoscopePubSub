'''
Created on Apr 11, 2015

@author: ronaldjosephdesmarais
'''
import requests,json

class PubSub_HTTP_API(object):
    
    def __init__(self,cfg):
        if cfg is None:
            #print "Configure Defaults localhost"
            self.protocol="http"
            self.host="localhost"
            self.port=8000
        else:
            self.protocol="http"
            self.host=cfg['host']
            self.port=cfg['http_port']
            #self.state="Open"
            #print "Load defaults from cfg file %s"%cfg
            
    def deletePublisher(self,pub_id):
        #print "Django_API::Delete Publisher %s"%pub_id
        data_json = requests.get('%s://%s:%s/pubsubservice/publisher_messaging/{"action":"delete","id":%s}'%(self.protocol,self.host,self.port,pub_id),cookies=None).text
        return data_json
        
    def createPublisher(self):
        #print "DJANGO_API::Create Publisher"
        #create json message, and send
        #create json message
        data_json = requests.get('%s://%s:%s/pubsubservice/create_publisher/{"method":"PublisherMessageQueue"}'%(self.protocol,self.host,self.port),cookies=None).text
        return json.loads(data_json)["id"]
        
        
    def createSubscriber(self):
        data_json = requests.get('%s://%s:%s/pubsubservice/create_subscriber/{"method":"SubscriberMessageQueue"}'%(self.protocol,self.host,self.port),cookies=None).text
        return json.loads(data_json)["id"]
    
    def createWSSubscriber(self,sub_ws_id):
        data_json = requests.get('%s://%s:%s/pubsubservice/create_subscriber/{"sub_ws_id":"%s","method":"WSSubscriberMessageQueue"}'%(self.protocol,self.host,self.port,sub_ws_id),cookies=None).text
        return json.loads(data_json)["id"]
    
    def deleteSubscriber(self,sub_id):
        #print "Django_API::Delete Publisher %s"%pub_id
        data_json = requests.get('%s://%s:%s/pubsubservice/subscriber_messaging/{"action":"delete","id":%s}'%(self.protocol,self.host,self.port,sub_id),cookies=None).text
        return data_json
    
    def getMessage(self,id):
        #http://localhost:8000/pubsubservice/subscriber_messaging/%7B%22id%22:1,%22action%22:%22retrieve%22,%22method%22:%22SubscriberMessageQueue%22%7D
        data_json = requests.get('%s://%s:%s/pubsubservice/subscriber_messaging/{"id":%s,"action":"retrieve","method":"SubscriberMessageQueue"}'%(self.protocol,self.host,self.port,id),cookies=None).text
        return data_json
    
    def createAssociation(self,pub_id,sub_id):
        #http://localhost:8000/pubsubservice/subscription/%7B%22pub_id%22:1,%22sub_id%22:1,%22action%22:%22subscribe%22%7D
        data_json = requests.get('%s://%s:%s/pubsubservice/subscription/{"pub_id":%s,"sub_id":%s,"action":"subscribe"}'%(self.protocol,self.host,self.port,pub_id,sub_id),cookies=None).text
        return data_json
           
    def sendMessage(self,msg,pub_id):
        #print "DJANGO_API::Send Message"
        data_json = requests.get('%s://%s:%s/pubsubservice/publisher_messaging/{"action":"send","id":%s,"msg":"%s","method":"PublisherMessageQueue"}'%(self.protocol,self.host,self.port,pub_id,msg),cookies=None).text
        return data_json
        
        