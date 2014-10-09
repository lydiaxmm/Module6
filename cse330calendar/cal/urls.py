from django.conf.urls.defaults import *
from tastypie.api import Api
from cal.api import CalResource, EventResource, UserResource

v1_api = Api(api_name='v1')
v1_api.register(CalResource())
v1_api.register(EventResource())
v1_api.register(UserResource())

from cal import views
 
urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    (r'^api/', include(v1_api.urls)),
)
