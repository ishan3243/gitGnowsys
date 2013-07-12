from django.db import models
import mobwrite.models
from django.contrib.auth.models import User
import objectapp.models
# Create your models here.

class SecurityCheck(models.Model):
	#an object which contains the details of drafts(mobwrite textobjs) and collaborating groups
	
	# Object properties:
  	# .baseVersion - the version of wikipage whose contents are being edited
  	# .pageid - reference to the wikipage
  	# .textobj - The shared text object being worked on.
  	# .owner - user who created a draft for a wikipage
  	# .sharedWith - other users with which this draft is shared (to be edited only)
	
        baseVersion=models.IntegerField()
	textobj=models.ForeignKey(mobwrite.models.TextObj)
	pageid=models.ForeignKey(objectapp.models.Gbobject)
	owner=models.ForeignKey(User, related_name="%(app_label)s_%(class)s_owner")
	sharedWith=models.ManyToManyField(User, through='CreatedOn')
	
	
class CreatedOn(models.Model):  #the intermediate table for the many to many field sharedWith    
	securityCheckObj=models.ForeignKey(SecurityCheck)
	invitedUser=models.ForeignKey(User)
	date_created=models.DateTimeField(auto_now_add=True)
	isRead=models.BooleanField(default=False)
	
