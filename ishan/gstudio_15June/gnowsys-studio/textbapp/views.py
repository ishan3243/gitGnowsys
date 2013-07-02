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
#from goto import goto,label


def checkOwnership2(request):
	if 'textObjName' in request.POST and request.POST['textObjName']:
		try:			
			securityCheckObj=SecurityCheck.objects.get(textobj__filename="_"+request.POST['textObjName'], owner=request.user.username)
			return HttpResponse(1)
		except:
			return HttpResponse(0)

def checkOwnership(request):
	if request.method=='POST' and request.POST['user'] and request.POST['owner']:
		return request.POST['user'] == request.POST['owner']

def deleteFx(request):
	if request.method=='POST' and 'textObjName' in request.POST and request.POST['textObjName']:
		try:
			securityCheckObj = SecurityCheck.objects.get(textobj__filename="_"+request.POST['textObjName'],owner=request.user.username)
			textObj=securityCheckObj.textobj
			securityCheckObj.delete()
			textObj.delete()
			return HttpResponse("DS")
		except SecurityCheck.DoesNotExist:
			raise Http404()
	else: 
		raise Http404()
			
def addRequestFx(request):
	if request.method=='POST':
		if 'textObjName' in request.POST and request.POST['textObjName'] and 'sentTo' in request.POST and request.POST['sentTo'] and request.user.is_authenticated():
			sentTo= request.POST['sentTo']
			textObjName= request.POST['textObjName']	 				
			filename="_"+textObjName			
			
			if sentTo==request.user.username:
				return HttpResponse("Can't send a request to yourself")				
									
		
			try:				
				uuu = User.objects.get(username=sentTo)			
				textobj=TextObj.objects.get(filename=filename)			
				securityCheckObj=SecurityCheck.objects.get(textobj=textobj,owner=request.user.username)			
				securityCheckObj.sharedWith.add(uuu)
				securityCheckObj.save()	
				return HttpResponse("request sent successfully")		
		
			except User.DoesNotExist:
				return HttpResponse("user does not exist! Please enter a valid username")
				
			except SecurityCheck.DoesNotExist:					
				return HttpResponse("bad internal failure!!!")
		
			except TextObj.DoesNotExist:		
				return HttpResponse("bad internal failure!!!")
							 
		else:
			return HttpResponse("invalid  details")
	else: 
		raise Http404()

def getUserListFx(request):
	
	userlist=[]
	for each in User.objects.all():
		userlist.append(each.username.__str__()+"  <"+each.email.__str__()+">")
        userListJson = json.dumps(userlist)
    	return HttpResponse(userListJson)
	
  

def mobwriteText(request):
	
	if request.method=='POST':
		q = urllib.unquote(request.raw_post_data)
   		mode = None
    		if q.find("p=") == 0:
        		mode = "script"
    		elif q.find("q=") == 0:
        		mode = "text"
    
	else:
	        return HttpResponseBadRequest("Missing q= or p=")
	#print "!!!!!!!!!!!!!!!!!!!!",q,"!!!!!!!!!!!!!!!!"
        q = q[2:]
        q1=q[q.find('\n')+1:len(q)]
        q1=q1[0:q1.find('\n')]
    	q1=q1[q1.find(':')+1:len(q1)]
    	q1=q1[q1.find(':')+1:len(q1)]   #this is the filename from the raw post data
	#print entryExists(q1)
	#print q1
	if not entryExists(q1):
		raise Http404()
		return HttpResponse()
	else:
		if isOwner(request,q1):
			return mobwrite.views.mobwrite(request)
		elif isSharedWith(request,q1):
			return mobwrite.views.mobwrite(request)
		else:
			raise Http404()
			return HttpResponse()

def getCurrentUsersFx(request):
	if request.method=='POST' and 'filename' in request.POST and request.POST['filename']:
		#print request.POST['filename']
		currUsers=ViewObj.objects.filter(filename=request.POST['filename']);
		curr=[];		
		for c in currUsers:
			curr.append(c.username)
		#print curr,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
		return HttpResponse(json.dumps(curr),content_type="application/json")
	else:
		raise Http404()
      
#display all groups
def getAllGroupsFx(request):
	if request.method=='POST' and 'filename' in request.POST and request.POST['filename'] and 'pageid' in request.POST and request.POST['pageid'] and request.user.is_authenticated():
		groupList=[]	
		try:
			securityCheckObjs=SecurityCheck.objects.filter(pageid=request.POST['pageid'])
			for s in securityCheckObjs:
				userlis=[]
				userlis.append(s.owner+"(owner/leader)")				
				try:				
						        					
					userlist=s.sharedWith.all()                          #get all the users for a particular group
					for u in userlist:							
						userlis.append(u.username)
			
					if s.textobj.filename=="_"+request.POST['filename']:	#the current user's group comes first
						groupList.insert(0,userlis)
			
					else:
						groupList.append(userlis)	
		
				except:
					groupList.append(userlis)
		
		except SecurityCheck.DoesNotExist:
			groupList=["No Groups are formed for editing this page "]

		return HttpResponse(json.dumps(groupList),content_type="application/json")
	else:
		raise Http404()

	
	
#def removeUser(request):
	

#KEY ASSUMPTION: each user can have only one draft for a page.

def entryExists(textObjName):
	name="_"+textObjName
	try:
		textObj=TextObj.objects.get(filename=name)
		return True
	except TextObj.DoesNotExist:
		return False	
			
def isOwner(request,textObjName):
	name="_"+textObjName
	try:
		securityCheckObj=SecurityCheck.objects.get(owner=request.user.username,textobj__filename=name)		
		return True
	except SecurityCheck.DoesNotExist:
		return False

def isSharedWith(request,textObjName):
	name="_"+textObjName
	try:
		securityCheckObj=SecurityCheck.objects.get(sharedWith__username=request.user.username,textobj__filename=name)
		return True
	except SecurityCheck.DoesNotExist:
		return False

def getTextObjName(request): #assume 
	pageid=request.POST['pageid']
	owner=request.POST['owner']
	try:
		securityCheckObj=SecurityCheck.objects.get(owner=owner,pageid=pageid,sharedWith__username=request.user.username)
		return securityCheckObj.textobj.filename[1:]
	except SecurityCheck.DoesNotExist:
		raise Http404()	
		
def get_or_insertTextObjName(request):
	
	def randomStringX(length):
	    s = ''
	    letters = "0123456789abcdefghijklmnopqrstuvwxyz"
	    while len(s) < length:
		s += letters[random.randint(0, len(letters)-1)]
	    return s

	def randomNameX():
	    name = randomString(10)
	    while TextObj.objects.filter(filename="_"+name).count() > 0:
		name = randomString(10)
	    return name
	
	pageid = request.POST['pageid']

	try:
		securityCheckObj=SecurityCheck.objects.get(owner=request.user.username,pageid=pageid)
		return securityCheckObj.textobj.filename[1:]
	except SecurityCheck.DoesNotExist:	
		name="_"+randomNameX()
		
		#textb,mobwrite
		try:
			o = TextObj(filename=name)
			o.save()   #possible Integrity Error			
			gbObj = Gbobject.objects.get(node_ptr_id=pageid)  #over-ride initial data with data from GBobjects
			o.text = gbObj.content_org
			o.save()
			securityCheckObj=SecurityCheck(pageid=pageid,owner=request.user.username,textobj=o)
			securityCheckObj.save()
			return name[1:]
		except Gbobject.DoesNotExist:	
			return "" 
	
	except:
		return ""

def editButtonFx(request):
	if request.method=='POST' and 'pageid' in request.POST and request.POST['pageid'] and request.user.is_authenticated():
		return HttpResponse(get_or_insertTextObjName(request))
	else :
		raise Http404()

def inviteAcceptFx(request):
	if request.method=='POST' and 'pageid' in request.POST and request.POST['pageid'] and 'owner' in request.POST and request.POST['owner'] and request.user.is_authenticated():
		return HttpResponse(getTextObjName(request))
	else:
                raise Http404()
