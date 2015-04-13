'''
Created on Feb 10, 2015

@author: ronaldjosephdesmarais
'''
from django.conf.urls import patterns, include, url

from pubsub import views 


urlpatterns = patterns('',
    # Examples:
    url(r'^subscriber_messaging/(?P<json_msg>.+)', views.subscriber_messaging, name='subscribe'),
    url(r'^publisher_messaging/(?P<json_msg>.+)', views.publisher_messaging, name='publish'), 
    url(r'^create_subscriber/(?P<json_msg>.+)', views.create_subscriber, name='create_subscriber'),
    url(r'^create_publisher/(?P<json_msg>.+)', views.create_publisher, name='create_publisher'),
    url(r'^subscription/(?P<json_msg>.+)', views.subscription, name='publish'), 
    # url(r'^pubsubservice/', include('pubsub.urls')),
    #url(r'^admin/', include(admin.site.urls)),
)