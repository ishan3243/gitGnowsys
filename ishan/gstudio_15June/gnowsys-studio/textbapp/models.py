from django.db import models
import mobwrite.models
from django.contrib.auth.models import User
# Create your models here.

class SecurityCheck(models.Model):
	textobj=models.ForeignKey(mobwrite.models.TextObj)
	owner=models.CharField(max_length=255)
	sharedWith=models.ManyToManyField(User)
	
	#def __init__(self,owner,filename,requestingUser):   
	#	models.Model.__init__(self)
	#	print 'hi1\n'		
	#	self.owner=owner
	#	print 'hi2\n'	
	#	self.textobj=mobwrite.models.TextObj.objects.get(filename=filename)
	#	print 'hi3\n'	
	#	self.sharedWith.add(User.objects.get(username=requestingUser))
	#	print 'hi4\n'	
 




