from tastypie.resources import ModelResource
from tastypie.paginator import Paginator
from cal.models import Cal, Event
from tastypie.fields import ToOneField, ForeignKey
from django.contrib.auth.models import User
from tastypie.authorization import Authorization
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import BasicAuthentication
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from django.contrib.sessions.models import Session
from django.conf.urls import url
from tastypie.resources import Resource
from tastypie.http import HttpUnauthorized, HttpForbidden
from tastypie.utils import trailing_slash
import json
import re
from cal.auth import *
from django.db import models


class MyAuthentication(BasicAuthentication):	
	def is_authenticated(self, request, **kwargs):
		if 'sessionid' in request.COOKIES:
			try:
				s = Session.objects.get(pk=request.COOKIES['sessionid'])
			except Exception,e:
				logger.warning("user with sessionid : %s not found" % request.COOKIES['sessionid'])
				return False

# get the user_id from the session
			if '_auth_user_id' in s.get_decoded():
# try to find the user associated with the given sessionid
				try:
					u = User.objects.get(pk=s.get_decoded()['_auth_user_id'])
					if u is not None:
						return True
				except Exception,e:
					return False
				else:
					return False
		else:
			logger.warning("sessionid is missing in the request")
			return False
			

class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		fields = ['first_name', 'last_name', 'email']
		allowed_methods = ['get', 'post']
		resource_name = 'user'
		authorization = UserObjectsOnlyAuthorization()

	def prepend_urls(self):
		return [
			url(r"^(?P<resource_name>%s)/login%s$" %
			(self._meta.resource_name, trailing_slash()),
			self.wrap_view('login'), name="api_login"),
		]
		

	def login(self, request, **kwargs):
		#index = str(request.body).index("username%22:%22")
		username = request.POST['username']
		password = request.POST['password']
	

		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				return self.create_response(request, {
					'success': True
				})
			else:
				return self.create_response(request, {
					'success': False,
					'reason': 'disabled',
					}, HttpForbidden )
		else:
			return self.create_response(request, {
				'success': False,
				'reason': 'incorrect',
				}, HttpUnauthorized )
		
		def getVal(self, index, s):
			length = len(s)
			substr = ""
			for i in range(index, length):
				if s[i]=='%':
					return substr
				else:
					substr += s[i]
					
class CalResource(ModelResource):
	user=ToOneField(UserResource, 'user',full=True)
	#user = model.ForeignKey(UserResource, 'username')
	class Meta:
		queryset = Cal.objects.all()
		paginator_class = Paginator
		authorization = CalAuth()
		#filtering={
		#	'username': ALL_WITH_RELATIONS,
		#}
	

class EventResource(ModelResource):
	cid = ToOneField(CalResource, "cal", full=True)
	user=ToOneField(UserResource, 'user',full=True)
	class Meta:
		queryset = Event.objects.all()
		paginator_class = Paginator
		always_return_data = True
		authorization = EventAuth()
		
	def dehydrate_cid(self, bundle):
		return bundle.obj.cal.id
		
	def hydrate_cid(self, bundle):
		bundle.data["cid"] = "/cal/%d/" % bundle.data["cid"]
		return bundle
	
	def dehydrate_user(self, bundle):
		return bundle.obj.user.id
		
	def hydrate_user(self, bundle):
		bundle.data["user"] = "/user/%d/" % bundle.request.user.id
		return bundle


	def hydrate_id(self, bundle):
		if bundle.data["id"] == 0:
			bundle.data["id"] = None
		return bundle


