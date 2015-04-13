'''
Created on Apr 5, 2015

@author: ronaldjosephdesmarais
'''

from twisted.internet.protocol import Factory
from twisted.internet import reactor
from TwistedWebsocket.server import Protocol  
from threading import Thread

from pubsub.api.pubsub_api import PubSub_HTTP_API

import re,json


class WebSocketHandler(Protocol):
    pub_sub_api=PubSub_HTTP_API(None)
    pub_sub_ids={}

    def onHandshake(self, header):
        g = re.search('Origin\s*:\s*(\S+)', header)
        if not g: return
        #print "\n[HANDSHAKE] %s origin : %s" % (self.id, g.group(1))

    #def onConnect(self):
    #    print "WS_SERVER::[CONNECTION] %s connected" % self.id

    def onDisconnect(self):
        pub_sub_obj=self.pub_sub_ids[self.id]
        if pub_sub_obj["Type"] == "Publisher":
            result = self.pub_sub_api.deletePublisher(pub_sub_obj["PubID"])
        elif pub_sub_obj["Type"] == "Subscriber":
            result = self.pub_sub_api.deleteSubscriber(pub_sub_obj["SubID"])

    def onMessage(self, str_msg):
        try:
            #print "WS_server::Decode %s"%str_msg
            msg_json = json.loads(str_msg)
            if msg_json["op"] == "createPublisher":
                pub_id = self.pub_sub_api.createPublisher()
                #print "WS_Server::Create Publisher id:%s:"%pub_id
                self.pub_sub_ids[self.id]={"PubID":pub_id,"Type":"Publisher"}
                self.users[self.id].sendMessage(('{"result":"success","id":%s}'%pub_id).encode("ascii"))
            elif msg_json["op"] == "createSubscriber":
                #print "Try to create Sub"
                sub_id = self.pub_sub_api.createWSSubscriber(self.id)
                #print "Created Sub %s"%sub_id
                self.pub_sub_ids[self.id]={"SubID":sub_id,"Type":"Subscriber"}
                self.users[self.id].sendMessage(('{"result":"success","id":%s}'%sub_id).encode("ascii"))
            elif msg_json["op"] == "sendMessageHttp":
                result = self.pub_sub_api.sendMessage(msg_json["message"],self.pub_sub_ids[self.id]["PubID"])
                self.users[self.id].sendMessage(result.encode("ascii"))
            elif msg_json["op"] == "sendMessageWebSocket":
                print "Great, now send %s to %s"%(msg_json["message"],msg_json["pub_ws_id"])
                pub_ws_id=msg_json["pub_ws_id"]
                message=msg_json["message"]
                self.users[pub_ws_id].sendMessage(message.encode("ascii"))
                #print "Send Message WebSocket"
            
        except Exception as e:
            self.users[self.id].sendMessage(('{"result":"failure","id":-1}').encode("ascii"))
            
      
    def sendMessageToWSSubscriber(self,id, msg):
        #print "Try to send message %s to %s"%(msg,id)
        for _id, user in self.users.items():
                #print "op:%s"%msg_json["op"]
                if _id == id:
                    user.sendMessage(msg.encode('ascii'))
                elif _id == self.id:
                    user.sendMessage("Ok Message Tried to Send Message")
                    
                
class WebSocketFactory(Factory):

    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        self.handler =  WebSocketHandler(self.users)
        return self.handler

class WebSocketServer(Thread):
    
    def __init__(self,web_socket_port):
        super(WebSocketServer,self).__init__(target=self.startWebSocketServer,args=(web_socket_port,))
    
    def startWebSocketServer(self,port):
        #print "WebSocketServer:: starting web socket server with %s"%port
        self.factory = WebSocketFactory()
        reactor.listenTCP(port, self.factory)
        reactor.run(installSignalHandlers=False)
    
    def getUsers(self):
        if hasattr(self.factory,"handler"):
            return self.factory.handler.users.items()
        else:
            return None
