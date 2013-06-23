# Create your views here.
import urllib
import socket

from django.conf import settings
from django.template import RequestContext

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.http import HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.utils import simplejson
from django.contrib.sites.models import Site
from django.http import Http404
from models import SecurityCheck
from mobwrite.models import *
from django.contrib.auth.models import User
import json
import mobwrite.views

def deleteFx(request):
	if request.method=='POST':
		if 'pageid' in request.POST and request.POST['pageid']:
			(TextObj.objects.filter(filename="_gnoweditor"+request.POST['pageid'])).delete()
	else: 
		raise Http404()
	return

def securityCheckFx(request):
	if request.method=='POST':
		if 'pageid' in request.POST and request.POST['pageid'] and 'owner' in request.POST and request.POST['owner']:
			 try:
				textobj=TextObj.objects.get(securitycheck__sharedWith=User.objects.get(username=request.user.username), filename__exact="_gnoweditor+"+request.POST['pageid']+"+"+request.POST['owner'])
                         	return HttpResponse(textobj.filename[1:len(textobj.filename)])
			 except TextObj.DoesNotExist:
				return HttpResponse("")
	else: 
		raise Http404()
	        return HttpResponse("")

def addRequestFx(request):
	print "!!!!!!!!!!!!!!!!!!!!in add request!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"	
	pageid= request.POST['pageid']
	owner= request.POST['owner']
	username= request.POST['username']
	if request.method=='POST':
		if 'pageid' in request.POST and request.POST['pageid'] and 'owner' in request.POST and request.POST['owner'] and 'username' in request.POST and request.POST['username']:
 			try:	
				print username+"hi try\n"		
				if username==owner:
					return HttpResponse("Can't send a request to yourself")	
				uuu = User.objects.get(username=username)
					
				print "hi try22222\n"			
				filename="_gnoweditor+"+str(pageid)+"+"+str(owner)				
				textobj=TextObj.objects.get(filename=filename)
				filename="_gnoweditor+"+str(pageid)+"+"+str(owner)
				print "\n!!!!"+filename+"!!!!\n"
				try:				
					securityCheckObj=SecurityCheck.objects.get(textobj=textobj,owner=owner)			
				except SecurityCheck.DoesNotExist:					
					securityCheckObj=SecurityCheck(textobj=textobj,owner=owner)
					securityCheckObj.save()	
				
				#if(SecurityCheck.objects.filter(owner=owner,sharedWith__username=username).exists()):
				#	print SecurityCheck.objects.filter(owner=owner,sharedWith__username=username)	
				#	print '#####!!!!!!!\n'				
				#	return HttpResponse("user already invited!")
								
				securityCheckObj.sharedWith.add(uuu)
				
				print securityCheckObj,"\n"
				securityCheckObj.save()			 
                        except User.DoesNotExist:
				print "except"
				return HttpResponse("user does not exist! Please enter a valid username")
			return HttpResponse("Request sent successfully!!")
	else: 
		raise Http404()

def getUserListFx(request):
	if request.method=='POST':
		
		userlist=User.objects.values('username')
		userlis=[]		
		for u in userlist:
			userlis.append(u['username']);
		HttpResponse(json.dumps(userlis))
	else:
		raise Http404()
	       
def mobwriteText(request):
	return mobwrite.views.mobwrite(request)
	if request.method=='POST':
		
			if (request.user.username==request.POST['owner']):
				return mobwrite.views.mobwrite(request)			 
			try:
				textobj=TextObj.objects.get(securitycheck__sharedWith=User.objects.get(username=request.user.username), filename__exact="_gnoweditor+"+request.POST['pageid']+"+"+request.POST['owner'])
                         	return mobwrite.views.mobwrite(request)
			 
			except TextObj.DoesNotExist:
				raise Http404()
			else: 
				raise Http404()
	else: 
		raise Http404()
