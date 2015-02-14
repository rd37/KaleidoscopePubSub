from django.contrib import admin

# Register your models here.
from pubsub.models import service_call,websocket_call,subscribers,publishers,subscriptions

#class servicelist_admin(admin.ModelAdmin):
    
class service_call_admin(admin.ModelAdmin):
    list_display = ('address','port','service')
    list_filter = ['address','port','service']
    
class websocket_call_admin(admin.ModelAdmin):
    list_display = ('webkey',)
    list_filter = ['webkey']

class subscribers_admin(admin.ModelAdmin):
    list_display = ('id','method','method_key')
    list_filter = ['id','method','method_key']
    
class publishers_admin(admin.ModelAdmin):
    list_display = ('id','method','method_key')
    list_filter = ['id','method','method_key']
    
class subscriptions_admin(admin.ModelAdmin):
    list_display = ('pubs','subs')
    list_filter = ['pubs','subs']
    
admin.site.register(service_call,service_call_admin)
admin.site.register(websocket_call,websocket_call_admin)
admin.site.register(subscribers,subscribers_admin)
admin.site.register(publishers,publishers_admin)
admin.site.register(subscriptions,subscriptions_admin)
