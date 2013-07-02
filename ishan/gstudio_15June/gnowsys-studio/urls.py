# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# Written 2009 by j@mailb.org
from os.path import join

from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^raw/(?P<name>.+)/', 'mobwrite.views.raw'),
    (r'^r/(?P<name>.+)/', 'mobwrite.views.raw'),
    (r'^m/(?P<name>.+)/', 'mobwrite.views.html'),
    (r'^t/(?P<name>.+)/', 'mobwrite.views.text'),
    (r'^$', 'app.views.index'),
    (r'^new/$', 'mobwrite.views.new'),
    (r'^mobwrite/', 'mobwrite.views.mobwrite'),
    

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^.bzr/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': join(settings.PROJECT_ROOT, ".bzr")}),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^%s(?P<path>.*)$' % settings.MEDIA_URL.lstrip('/'),
                               'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT}),
    )

