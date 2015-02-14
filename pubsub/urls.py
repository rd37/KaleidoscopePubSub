'''
Created on Feb 10, 2015

@author: ronaldjosephdesmarais
'''
from django.conf.urls import patterns, include, url

from pubsub import views 


urlpatterns = patterns('',
    # Examples:
    url(r'^subscribe/(?P<json_msg>.+)', views.subscribe, name='subscribe'),
    url(r'^publish/(?P<json_msg>.+)', views.publish, name='publish'),
    url(r'^subscription/(?P<json_msg>.+)', views.subscription, name='publish'), 
    # url(r'^pubsubservice/', include('pubsub.urls')),
    #url(r'^admin/', include(admin.site.urls)),
)