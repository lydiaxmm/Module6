from django.db import models
from django.contrib.auth.models import User
# Extensible wants two models: a "calendar" model and an "event" model.
# The "calendar" model represents a collection of events.  Note that the end
# application supports multiple calendars in the same view, with the events
# in each calendar having a different background color.
# 
# First we will define our calendar model, `Cal`, and then we will define
# our event model, `Event`.
 
class Cal(models.Model):
	# Title of the calendar
	title = models.CharField(max_length=50)
	
	user = models.ForeignKey(User)

	# Text description of the calendar
	description = models.CharField(max_length=200)

	 # Color ID (1-32)
	color = models.IntegerField(default=1)

	# Boolean for whether the calendar is hidden by default
	hidden = models.BooleanField(default=False)

class Event(models.Model):
	# Declare a one-to-many relationship with Cal
	cal = models.ForeignKey(Cal)

	user = models.ForeignKey(User)
	# Title of the event
	title = models.CharField(max_length=50)

	# DateTime of event start
	start = models.DateTimeField()

	# DateTime of event end
	end = models.DateTimeField()

	# Additional information that can be associated with an event:
	loc = models.CharField(max_length=50) # Location
	notes = models.CharField(max_length=200) # Notes
	url = models.CharField(max_length=100) # URL
	ad = models.BooleanField(default=False) # Is this an all-day event
	rem = models.CharField(max_length=200) # Reminder
