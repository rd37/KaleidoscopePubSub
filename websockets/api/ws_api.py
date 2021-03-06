'''
Created on Apr 12, 2015

@author: ronaldjosephdesmarais
'''

from websocket import create_connection
import json,thread

class PubSub_WS_API(object):
    
    def __init__(self,cfg):
        #print "Create WS api"
        if cfg is None:
            #Use defaults for config
            self.host="127.0.0.1"
            self.port=8001
            self.protocol="ws"
            self.ws = None
            self.state="Open"
        else:
            self.protocol="ws"
            self.host=cfg['host']
            self.port=cfg['ws_port']
            self.state="Open"
            self.ws=None
            #print "Load cfg file and configure"
    
    def createSubscriber(self):
        if self.ws is None:
            self.ws = create_connection("%s://%s:%s"%(self.protocol,self.host,self.port))
            self.ws.send('{"op":"createSubscriber"}')
            result =  self.ws.recv()
            self.state="Subscriber"
            return json.loads(result)["id"]
        else:
            return "Publisher Subscriber Already Exists"
        
    def createPublisher(self):
        if self.ws is None:
            #print "Create Publisher %s://%s:%s"%(self.protocol,self.host,self.port)
            self.ws = create_connection("%s://%s:%s"%(self.protocol,self.host,self.port))
            self.ws.send('{"op":"createPublisher"}')
            result =  self.ws.recv()
            self.state="Publisher"
            return json.loads(result)["id"]
        else:
            return "Publisher Already Exists"
        
    def closeConnection(self):
        if self.ws is not None:
            self.ws.close()
            self.state="Open"
        else:
            return "No Publisher or Subscriber exists"
    
    
    def sendSyncMessage(self,msg):
        if self.state is "Publisher":
            self.ws.send('{"op":"sendMessageHttp","message":"%s"}'%msg)
            result =  self.ws.recv()
            return result
    
    def pushSubscriberMessage(self,msg,pub_ws_id):
        #print "Create WS Connection and send %s to %s"%(msg,pub_ws_id)
        #print "%s://%s:%s"%(self.protocol,self.host,self.port)
        self.ws = create_connection("%s://%s:%s"%(self.protocol,self.host,self.port))
        #print "WS_API sending now"
        self.ws.send('{"op":"sendMessageWebSocket","message":"%s","pub_ws_id":"%s"}'%(msg,pub_ws_id))
        #print "WS_API done sending %s"%msg
        
    def retreiveSyncMessage(self):
        return self.ws.recv()   
    
    def retreiveASyncMessage(self,cb):
        thread.start_new_thread(self._rcv_callback, (cb,))
        
    def _rcv_callback(self,cb):
        cb.async_callback(self.ws.recv())
        #self._rcv_callback(cb)
    
    def registerASyncMessageCallback(self,cb):
        thread.start_new_thread(self._rcv_callback_recursive, (cb,))
        
    def _rcv_callback_recursive(self,cb):
        try:
            cb.async_callback(self.ws.recv())
            self._rcv_callback_recursive(cb)
        except Exception as e:
            print "Recursive Exception occured on thread, leaving %s"%e
        
        
        