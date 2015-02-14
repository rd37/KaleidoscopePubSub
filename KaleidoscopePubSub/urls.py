from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'KaleidoscopePubSub.views.home', name='home'),
    url(r'^pubsubservice/', include('pubsub.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
