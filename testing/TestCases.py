'''
Created on Apr 12, 2015

@author: ronaldjosephdesmarais
'''
import unittest
from websockets.api.ws_api import PubSub_WS_API
from pubsub.api.pubsub_api import PubSub_HTTP_API

import time

class Test(unittest.TestCase):


    def setUp(self):
        self.ws_api = PubSub_WS_API(None)
        self.ws_api_sub = PubSub_WS_API(None)
        self.http_api = PubSub_HTTP_API(None)
        self.create_pub_result=self.http_api.createPublisher()
        print "Test Setup Create Publisher over HTTP Result %s"%self.create_pub_result
        pass


    def tearDown(self):
        self.http_api.deletePublisher(self.create_pub_result)
        self.ws_api.closeConnection()
        self.ws_api_sub.closeConnection()
        print "Test Delete HTTP Created Publisher"
        pass


    def testCreateWS_Publisher(self):
        #print "test Create Publisher"
        self.id = self.ws_api.createPublisher()
        #print "Test create WS publisher Got back %s"%self.id
        assert self.id > 0
        pass
    
    def testSendMessageWS_Publisher(self):
        #print "test Send Message"
        self.id = self.ws_api.createPublisher()
        result = self.ws_api.sendSyncMessage("hey there, glad to hear from you")
    #    print "Test Send WS Publisher Message Got back %s"%result
        assert result > 0
    
    def testSendMessageWS_Pub_HTTP_Sub(self):
        pub_id = self.ws_api.createPublisher()
        sub_id = self.http_api.createSubscriber()
        res = self.http_api.createAssociation(pub_id, sub_id)
        self.ws_api.sendSyncMessage("ws publisher says hey there")
        sub_msg = self.http_api.getMessage(sub_id)
    #    print "Test WS Pub HTTP Sub and Got Message %s"%sub_msg
        self.http_api.deleteSubscriber(sub_id)
        assert "hey there" in sub_msg
        
        
    def testSendMessageWS_Pub_WS_Sub(self):
        pub_id = self.ws_api.createPublisher()
        sub_id = self.ws_api_sub.createSubscriber()
        #print "Got pub %s and sub %s"%(pub_id,sub_id)
        res = self.http_api.createAssociation(pub_id, sub_id)
        #print "Subscription %s Now Send Message"%res
        self.ws_api.sendSyncMessage("ws publisher says boomra")
        sub_msg = self.ws_api_sub.retreiveSyncMessage()
        #print "Test WS Pub and WS Sub and Got Message %s"%sub_msg
        assert "boom" in sub_msg
    
    def testSendAsyncMessagesMulti(self):
        pub_id = self.ws_api.createPublisher()
        http_api2 = PubSub_HTTP_API(None)
        pub_id1 = http_api2.createPublisher()
        
        sub_id = self.ws_api_sub.createSubscriber()
        ws_api_sub2 = PubSub_WS_API(None)
        sub_id2 = ws_api_sub2.createSubscriber()
        http_api_sub3 = PubSub_HTTP_API(None)
        sub_id3 = http_api_sub3.createSubscriber()
        
        self.wait=None
        
        self.ws_api_sub.retreiveASyncMessage(self)
        #ws_api_sub2.retreiveASyncMessage(self)
        #print "Got pub %s and sub %s"%(pub_id,sub_id)
        self.http_api.createAssociation(pub_id, sub_id)
        self.http_api.createAssociation(pub_id, sub_id2)
        self.http_api.createAssociation(pub_id, sub_id3)
        
        self.http_api.createAssociation(pub_id1, sub_id2)
        self.http_api.createAssociation(pub_id1, sub_id3)
        
        #print "Subscription %s Now Send Message"%res
        self.ws_api.sendSyncMessage("ws publisher says boomra")
        #print "Now wait"
        while self.wait is None:
            time.sleep(1)
        assert "boom" in self.wait
        
        self.wait=None
        ws_api_sub2.retreiveASyncMessage(self)
        while self.wait is None:
            time.sleep(1)
        
        #print "Test WS Pub and WS Sub and Got Message %s"%sub_msg
        assert "boom" in self.wait
        
        msg=http_api_sub3.getMessage(sub_id3)
        
        assert "boom" in msg
        #print "done"
        http_api2.deletePublisher(pub_id1)
        
        pass
    
    def testSendAsyncMessageWS_Pub_WS_Sub(self):
        pub_id = self.ws_api.createPublisher()
        sub_id = self.ws_api_sub.createSubscriber()
        self.wait=None
        self.ws_api_sub.retreiveASyncMessage(self)
        #print "Got pub %s and sub %s"%(pub_id,sub_id)
        res = self.http_api.createAssociation(pub_id, sub_id)
        #print "Subscription %s Now Send Message"%res
        self.ws_api.sendSyncMessage("ws publisher says boomra")
        #print "Now wait"
        while self.wait is None:
            time.sleep(1)
        #print "Test WS Pub and WS Sub and Got Message %s"%sub_msg
        assert "boom" in self.wait
        #print "done"
        pass
    
    def testSendAsyncMessageCallbackWS_Pub_WS_Sub(self):
        pub_id = self.ws_api.createPublisher()
        sub_id = self.ws_api_sub.createSubscriber()
        self.wait=None
        self.ws_api_sub.registerASyncMessageCallback(self)
        #print "Got pub %s and sub %s"%(pub_id,sub_id)
        res = self.http_api.createAssociation(pub_id, sub_id)
        #print "Subscription %s Now Send Message"%res
        self.ws_api.sendSyncMessage("ws publisher says boomra")
        #print "Now wait"
        while self.wait is None:
            time.sleep(1)
        #print "Test WS Pub and WS Sub and Got Message %s"%sub_msg
        assert "boom" in self.wait
        
        self.wait = None
        self.ws_api.sendSyncMessage("ws publisher says baamra")
        #print "Now wait"
        while self.wait is None:
            time.sleep(1)
        #print "Test WS Pub and WS Sub and Got Message %s"%sub_msg
        assert "baam" in self.wait
        
        #print "done"
        pass
        
    def async_callback(self,msg):
        #print "async_cb got %s"%msg
        self.wait=msg

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()