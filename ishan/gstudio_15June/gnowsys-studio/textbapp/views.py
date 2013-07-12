# Create your views here.
import urllib
import socket
from django.shortcuts import redirect
from django.conf import settings
from django.template import RequestContext

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.http import HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.utils import simplejson
from django.contrib.sites.models import Site
from django.http import Http404
from models import *
from mobwrite.models import *

from objectapp.models import Gbobject,System
from django.contrib.auth.models import User
import json
import mobwrite.views
import models
from gstudio.models import NID
from reversion import *
#from goto import goto,label


#KEY ASSUMPTION: each user can have only one draft for a page.

# method to get all invitations/requests a user received from 
# and sent to other users for a specific page
def getCollabRequestsandSentToFx(request,pageid):
	   
   userlis=[]
   pageRequests=[]
   if (request.user.is_authenticated()):
     
      user=User.objects.get(username=request.user.username)
      
      securityCheckObj=SecurityCheck.objects.filter(pageid__node_ptr_id=pageid,sharedWith__username=request.user.username);         
	
      for t in securityCheckObj:
         owner=t.owner.username
         pageRequests.append(owner)
      
      if not securityCheckObj:
         pageRequests.append("No collaboration requests.")
      
      #display all invitees
      #userlis=[]		
      try:		
         securityCheckObj=SecurityCheck.objects.get(owner__username=request.user.username,pageid__node_ptr_id=pageid)
	 userlist=securityCheckObj.sharedWith.all()  #returns a list of User objects.
	 if(not userlist):
	 	userlis=['You have not invited anyone yet.']
	 	randomThing=1			# used as a status
	 else:
	 	randomThing=2
	 	
	 for u in userlist:
	    userlis.append(u.username)
      except:
	 userlis=["You have no drafts saved for this page."]
         randomThing=0
         
   page_ob = System.objects.get(id=pageid) 
   currVersion=0
   for x in page_ob.ref.get_ssid:
   	currVersion+=1 
   

   jsonObj=json.dumps([pageRequests,userlis,currVersion,randomThing])	
   return HttpResponse(jsonObj,content_type="application/json") 


# deletes a draft of a user for a specific page
def deleteFx(request):
	if request.method=='POST' and 'textObjName' in request.POST and request.POST['textObjName']:
		try:
			securityCheckObj = SecurityCheck.objects.get(textobj__filename="_"+request.POST['textObjName'],owner__username=request.user.username)
			textObj=securityCheckObj.textobj
			securityCheckObj.sharedWith.clear()
			securityCheckObj.delete()
			textObj.delete()
			return HttpResponse("DS")		#delete successful
		except SecurityCheck.DoesNotExist:		
			return HttpResponse("DNS")		#delete not successful
	else: 
		raise Http404()
		
		
# makes entry in SecurityObj when a user invites another user
def addRequestFx(request):
	if request.method=='POST':
		if 'textObjName' in request.POST and request.POST['textObjName'] and 'sentTo' in request.POST and request.POST['sentTo'] and request.user.is_authenticated():
			sentTo= request.POST['sentTo']	 				
			filename="_"+request.POST['textObjName']			
			
			if sentTo==request.user.username:
				return HttpResponse("Can't send a request to yourself")				
									
		
			try:				
				uuu = User.objects.get(username=sentTo)				
				securityCheckObj=SecurityCheck.objects.get(textobj__filename=filename,owner__username=request.user.username)
				
				co=CreatedOn.objects.get(securityCheckObj=securityCheckObj,invitedUser__username=sentTo)
				return HttpResponse("Request already sent")
					
							
			except CreatedOn.DoesNotExist:
				obj=CreatedOn(securityCheckObj=securityCheckObj,invitedUser=uuu)
				obj.save()	
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


# retrieve list of all registered users
def getUserListFx(request):
	
	userlist=[]
	for each in User.objects.all():
		userlist.append(each.username.__str__())
        userListJson = json.dumps(userlist)
    	return HttpResponse(userListJson)
	
  
# guard at the gateway to mobwrite
# all the requests are first processed for validity in SecurityCheck table
# and then sent to mobwrite if valid
# valid in 2 cases:
#  1. owner of draft requests his draft(textobj) or creates a new one if not present
#  2. other user requests a draft(textobj) that is shared with him
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



# retrieve all the online users editing a specific draft(textobj)
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
      

      
# retrieve all groups created for a specific wikipage
def getAllGroupsFx(request):
	if request.method=='POST' and 'filename' in request.POST and request.POST['filename'] and 'pageid' in request.POST and request.POST['pageid'] and request.user.is_authenticated():
		groupList=[]	
		try:
			securityCheckObjs=SecurityCheck.objects.filter(pageid__node_ptr_id=request.POST['pageid'])
			for s in securityCheckObjs:
				userlis=[]
				userlis.append(s.owner.username.__str__()+"(owner/leader)  '<'"+User.objects.get(username=s.owner.username).email.__str__()+"'>'")				
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

	
# checks if textobj of this filename exits
def entryExists(textObjName):
	name="_"+textObjName
	try:
		textObj=TextObj.objects.get(filename=name)
		return True
	except TextObj.DoesNotExist:
		return False	

# checks if this user is owner of this textobj			
def isOwner(request,textObjName):
	name="_"+textObjName
	try:
		securityCheckObj=SecurityCheck.objects.get(owner__username=request.user.username,textobj__filename=name)		
		return True
	except SecurityCheck.DoesNotExist:
		return False

# checks if this textobj is shared with this user
def isSharedWith(request,textObjName):
	name="_"+textObjName
	try:
		securityCheckObj=SecurityCheck.objects.get(sharedWith__username=request.user.username,textobj__filename=name)
		return True
	except SecurityCheck.DoesNotExist:
		return False

# retrieve textobj(draft) name for this page
def getTextObjName(request):			 # called only for users other than owner of the draft(invited users)
	pageid=request.POST['pageid']
	owner=request.POST['owner']
	try:
		securityCheckObj=SecurityCheck.objects.get(owner__username=owner,pageid__node_ptr_id=pageid,sharedWith__username=request.user.username)
		return securityCheckObj.textobj.filename[1:]
	except SecurityCheck.DoesNotExist:
		raise Http404()	
		
# retrieve textobj(draft) name or create a textobj for this page	
def get_or_insertTextObjName(request):		 # called only for owner of draft
	
	#following two local methods to generate a random name for textobj
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
		securityCheckObj=SecurityCheck.objects.get(owner__username=request.user.username,pageid__node_ptr_id=pageid)
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
			
			page_ob = System.objects.get(id=pageid)
			baseVersion=0
  			for x in page_ob.ref.get_ssid:
   				baseVersion+=1 
			
			securityCheckObj=SecurityCheck(pageid=gbObj,owner=User.objects.get(username=request.user.username),textobj=o,baseVersion=baseVersion)
			print "sc 22222"
			securityCheckObj.save()
			return name[1:]
		except Gbobject.DoesNotExist:
			return "" 
	
	except:
		return ""

# method called to respond to ajax request when edit button is clicked
# sends the name of a textobj
def editButtonFx(request):
	if request.method=='POST' and 'pageid' in request.POST and request.POST['pageid'] and request.user.is_authenticated():
		return HttpResponse(get_or_insertTextObjName(request))
	else :
		raise Http404()


# method called to respond to ajax request when an invitation request is clicked
# sends the name of a textobj
def inviteAcceptFx(request):
	if request.method=='POST' and 'pageid' in request.POST and request.POST['pageid'] and 'owner' in request.POST and request.POST['owner'] and request.user.is_authenticated():
		return HttpResponse(getTextObjName(request))
	else:
                raise Http404()
                

# method that fetches all notifications(invitation requests for every page if exist)
def fetchRequestsFx(request):
	if request.method=='POST' and request.user.is_authenticated():
   		pageRequests=[]
		user=User.objects.get(username=request.user.username)
		try:  
         		 securityCheckObj=SecurityCheck.objects.filter(sharedWith__username=request.user.username).order_by('-createdon__date_created');         
	
			 for t in securityCheckObj:
			    title=NID.objects.get(id=t.pageid.node_ptr_id).title
			    co=CreatedOn.objects.get(securityCheckObj=t, invitedUser__username=request.user.username)
			    isRead=co.isRead
			    print isRead
			    pageRequests.append([t.owner.username,t.pageid.node_ptr_id,title,isRead])
		except SecurityCheck.DoesNotExist:
		   print "hipagepyheader" 
		finally:
		   print "finallyheader"
		pageRequestsJson = json.dumps(pageRequests)
    		return HttpResponse(pageRequestsJson,content_type="application/json")
	else: 
		raise Http404()
	
# Notification Handling Code
# changes status of notification from read to unread
def markReadFx(request):
	if request.method=='POST' and 'owner' in request.POST and 'pageid' in request.POST:
		try:
			securityCheckObj=SecurityCheck.objects.get(owner__username=request.POST['owner'],sharedWith__username=request.user.username,pageid__node_ptr_id=request.POST['pageid'])
			
			co=CreatedOn.objects.get(securityCheckObj=securityCheckObj, invitedUser__username=request.user.username)
			co.isRead=True
			co.save()
			return HttpResponse('/gstudio/page/gnowsys-page/'+str(request.POST['pageid']))
		except SecurityCheck.DoesNotExist:
			return HttpResponse("something wrong")
	else:
		raise Http404()	
		
		
# unshare a draft(textobj) from a user previously invited		
def unshareFx(request):
	if request.method=='POST' and 'pageid' in request.POST and 'user' in request.POST:
		try:
			securityCheckObj=SecurityCheck.objects.get(pageid__node_ptr_id=request.POST['pageid'],owner__username=request.user.username)

			co=CreatedOn.objects.get(securityCheckObj=securityCheckObj,invitedUser__username=request.POST['user'])
			co.delete()
			return HttpResponse('success')
			
		except:
			raise Http404	
	else:
		raise Http404()

# retrieve base version(version of page from where draft was created)
def getBaseVersionFx(request):
	print "hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii"
	try:
		ver=SecurityCheck.objects.get(textobj__filename="_"+str(request.POST['textObjName'])).baseVersion
		return HttpResponse(ver)
	except:
		return HttpResponse("error")
