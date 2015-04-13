'''
Created on Apr 7, 2015

@author: ronaldjosephdesmarais
'''
from ws_api import PubSub_WS_API

api = PubSub_WS_API(None)
id = api.createPublisher()
result = api.sendSyncMessage("hey there, glad to hear from you")
print result
api.closeConnection()