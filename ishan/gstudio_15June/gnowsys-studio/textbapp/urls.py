from django.conf.urls.defaults import url
from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import *
from registration.views import register

from gstudio.forms import RecaptchaRegistrationForm

urlpatterns = patterns(
    '',
    (r'^raw/(?P<name>.+)/', 'mobwrite.views.raw'),
    (r'^r/(?P<name>.+)/', 'mobwrite.views.raw'),
    (r'^m/(?P<name>.+)/', 'mobwrite.views.html'),
    #(r'^t/(?P<name>.+)/', 'mobwrite.views.text'),
    #(r'^$', 'app.views.index'),
    #(r'^new/$', 'mobwrite.views.new'),
    (r'^mobwrite/', 'textbapp.views.mobwriteText'), 
    #(r'^test/', test_view), 
    #(r'^synclink/$','mobwrite.views.syncfx'),
    (r'^deleteLink/$','textbapp.views.deleteFx'),
    (r'^editButton/$','textbapp.views.editButtonFx'),
    (r'^invitationAccept/$','textbapp.views.inviteAcceptFx'),
   # (r'^securityCheck/$','textbapp.views.securityCheckFx'),
    (r'^addRequest/$','textbapp.views.addRequestFx'),
    (r'^getUserList/$','textbapp.views.getUserListFx'),
    (r'getCurrentUsers/$','textbapp.views.getCurrentUsersFx'),
    (r'^getAllGroups/$','textbapp.views.getAllGroupsFx'),
)
