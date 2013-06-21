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
import models
import mobwrite.models

def deleteFx(request):
	if request.method=='POST':
		if 'pageid' in request.POST and request.POST['pageid']:
			(mobwrite.models.TextObj.objects.filter(filename="_gnoweditor"+request.POST['pageid'])).delete()
	else: 
		raise Http404
	return
