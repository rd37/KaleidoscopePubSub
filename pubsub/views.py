from django.http import HttpResponse
from django.shortcuts import RequestContext
from django.template import loader

import json

from pubsub.models import service_call,websocket_call,message_queue,subscribers,publishers,subscriptions
from pubsub.utils.tools import PublisherMessageQueue, SubscriberMessageQueue , WSSubscriberMessageQueue 
from websockets.web_socket_server import WebSocketServer

import random,logging

#logging
log = logging.getLogger('glint_api')
fh = logging.FileHandler('pubsub.log')
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
log.addHandler(fh)

log.info("**** Starting Service ****")

msg_queues = {}
subs = subscribers.objects.all()
pubs = publishers.objects.all()
subscriptS = subscriptions.objects.all()

#add support for publisher subscriber with websockets
web_socket_server = WebSocketServer(8001)
web_socket_server.start()

for sub in subs:
    #print "Sub %s"%sub
    key = sub.method_key
    method = sub.method
    #obj = eval(method)
    obj_class = globals()[method]
    msg_queues["%s"%key]=obj_class(object)
    
for pub in pubs:
    #print "Pub %s"%pub
    key = pub.method_key
    method = pub.method
    obj_class = globals()[method]
    msg_queues["%s"%key]=obj_class(object)

for subscripts in subscriptS:
    logging.debug( "boomra %s"%subscripts )
    sub_key = subscripts.subs.pk
    pub_key = subscripts.pubs.pk
    subscriber = subscribers.objects.filter(pk=sub_key)
    publisher = publishers.objects.filter(pk=pub_key)
    mq_pub = msg_queues["%s"%publisher[0].method_key]
    mq_sub = msg_queues["%s"%subscriber[0].method_key]
    mq_pub.subscribe(mq_sub)
    
# Create your views here.
def generateOutput(request,page,data):
    template = loader.get_template(page)
    context =  RequestContext(request, data)
    return template.render(context)

def createRandomKey():
    hash_key = random.getrandbits(128)
    while hash_key in msg_queues:
        #print "key in Use try another "
        hash_key = random.getrandbits(128)
    return hash_key

def create_publisher(request,json_msg):
    log.debug("DJANGO::create publisher")
    #print("DJANGO::create publisher")
    j_obj=json.loads(json_msg)
    
    if j_obj["method"] == "PublisherMessageQueue":
        m = PublisherMessageQueue(100)
        h_key = createRandomKey()
        msg_queues["%s"%h_key]=m
    p = publishers(method=j_obj["method"],method_key=h_key)
    p.save()
    #socket_users = web_socket_server.getUsers()
    #print "Return publisher"
            
    return HttpResponse(generateOutput(request,'jsons/results.json',{"result":"Created New Publisher","id":"%s"%p.pk}))
    
def publisher_messaging(request,json_msg):
    log.debug( "length %s New Message queues: %s"%(len(msg_queues),msg_queues) )
    #print "DJNAGO::PUBMSGING::Message %s"%json_msg
    j_obj=json.loads(json_msg)
    publisher = publishers.objects.filter(pk=j_obj["id"])
    #print "pub messaging %s"%j_obj
    if len(publisher) > 0:
        #print "found publisher, update it/use it"
        if j_obj["action"] == "send":
            #print "DJANGO::send message via publisher using %s"%j_obj
            publisher[0].send(j_obj,msg_queues)
            return HttpResponse(generateOutput(request,'jsons/results.json',{"result":"Send Message"}))
        elif j_obj["action"] == "delete":
            #print "DJAGNO::Remove from %s"%msg_queues
            del msg_queues["%s"%publisher[0].method_key]
            publisher[0].delete()
            return HttpResponse(generateOutput(request,'jsons/results.json',{"result":"Deleted Publisher"}))
        else:
            #print "Error Updating/Using Publisher"
            return HttpResponse(generateOutput(request,'jsons/results.json',{"result":"Error Action Command should be send or delete"}))
    else:
        
        return HttpResponse(generateOutput(request,'jsons/results.json',{"result":"Error Publisher Id does not exist"}))

def create_subscriber(request,json_msg):
    log.debug( "create new subscriber" )
    #print "Create subscriber %s"%json_msg
    j_obj=json.loads(json_msg)
    if j_obj["method"] == "SubscriberMessageQueue":
        m = SubscriberMessageQueue(100)
        h_key = createRandomKey()
        msg_queues["%s"%h_key]=m
    elif j_obj["method"] == "WSSubscriberMessageQueue":
        m = WSSubscriberMessageQueue(j_obj["sub_ws_id"])
        h_key = createRandomKey()
        msg_queues["%s"%h_key]=m
    s = subscribers(method=j_obj["method"],method_key=h_key)
    s.save()
    return HttpResponse(generateOutput(request,'jsons/results.json',{"result":"Created New Subscriber","id":"%s"%s.pk}))
    
def subscriber_messaging(request,json_msg):
    log.debug( "length %s New Message queues: %s"%(len(msg_queues),msg_queues) )
    j_obj=json.loads(json_msg)
    sub_id = j_obj["id"]
    subs = subscribers.objects.filter(pk=sub_id)
    if len(subs) > 0:
        if j_obj["action"] == "retrieve":
            msg = subs[0].retrieve(j_obj,msg_queues)
            return HttpResponse(generateOutput(request,'jsons/messages.json',{"result":"Retrieve Message","message":"%s"%msg}))
        elif j_obj["action"] == "delete":
            #print "Remove from %s"%msg_queues
            del msg_queues["%s"%subs[0].method_key]
            subs[0].delete()
            return HttpResponse(generateOutput(request,'jsons/results.json',{"result":"Deleted Subscriber"}))
        else:
            #print "Error Updating/Using Publisher"
            return HttpResponse(generateOutput(request,'jsons/results.json',{"result":"Error Action Command should be retrieve or delete"}))
    else:
        return HttpResponse(generateOutput(request,'jsons/results.json',{"result":"Error Subscriber id is Incorrect"}))
        
def subscription(request,json_msg):
    #print "Create Subscripton %s"%json_msg
    j_obj=json.loads(json_msg)
    sub_id = j_obj["sub_id"]
    pub_id = j_obj["pub_id"]
    subscriber = subscribers.objects.filter(pk=sub_id)
    publisher = publishers.objects.filter(pk=pub_id)
    if len(subscriber) > 0 and len(publisher) > 0:
        if j_obj["action"] == "subscribe":
            #print "add subscriber to publisher messages"
            mq_sub = msg_queues["%s"%subscriber[0].method_key]
            mq_pub = msg_queues["%s"%publisher[0].method_key]
            s = subscriptions.objects.filter(pubs=publisher[0],subs=subscriber[0])
            if len(s) > 0:
                return HttpResponse(generateOutput(request,'jsons/results.json',{"result":"Error Subscription Already Exists"}))
            mq_pub.subscribe(mq_sub)
            s = subscriptions(pubs=publisher[0],subs=subscriber[0])
            s.save()
            return HttpResponse(generateOutput(request,'jsons/results.json',{"result":"Success adding a subscription"}))
        elif j_obj["action"] == "unsubscribe":
            print "Unsubscribe"
            mq_sub = msg_queues["%s"%subscriber[0].method_key]
            mq_pub = msg_queues["%s"%publisher[0].method_key]
            mq_pub.unsubscribe(mq_sub)
            s = subscriptions.objects.filter(pubs=publisher[0],subs=subscriber[0])
            s.delete()
            return HttpResponse(generateOutput(request,'jsons/results.json',{"result":"Success Unsubscribing"}))
    else:
        return HttpResponse(generateOutput(request,'jsons/results.json',{"result":"Error Applying Subscription"}))
    
