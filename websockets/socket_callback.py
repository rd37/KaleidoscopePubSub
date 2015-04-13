'''
Created on Apr 5, 2015

@author: ronaldjosephdesmarais
'''
from websocket import create_connection
import json

#manipulate tables
def callback(msg):
    print "Socket CB Received %s"%msg
    
    
def send_sock_msg(id_sock,msg):
    js_msg = dict()
    js_msg["op"]="snd_msg"
    js_msg["id"]=id_sock
    js_msg["sock_msg"]="youstill"
    #js_msg={'id':'%'%id_sock,'msg':'%s'%msg}
    ws = create_connection("ws://localhost:8001/websocket")
    #print "Sending 'Hello, World'..."
    ws.send("%s"%json.dumps(js_msg))
    #ws.send('{"msg":"blah"}')
    print "Sent"
    print "Receiving..."
    result =  ws.recv()
    print "Received '%s'" % result
    ws.close()