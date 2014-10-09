from django.conf.urls import patterns, include, url
from cal.api import CalResource, EventResource, UserResource
 
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
 
# RESTful setup:
cal_resource = CalResource()
event_resource = EventResource()
user_resource = UserResource()
 
urlpatterns = patterns('',
    # Admin page
    url(r'^admin/', include(admin.site.urls)),
 
    # Templates
    url(r'^', include('cal.urls')),
 
    # RESTful URLs
    url(r'^', include(cal_resource.urls)),
    url(r'^', include(event_resource.urls)),
    url(r'^', include(user_resource.urls)),
)
