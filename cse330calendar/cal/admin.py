from django.contrib import admin
 
# We will create these models in the next step
from cal.models import Cal, Event
 
admin.site.register(Cal)
admin.site.register(Event)
