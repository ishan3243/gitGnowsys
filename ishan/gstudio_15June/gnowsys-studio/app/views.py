# Create your views here.
import urlparse

from django.template import RequestContext

from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404


def index(request):
    url = request.build_absolute_uri(request.path)
    domain = urlparse.urlsplit(url)[1]
    context = RequestContext(request, {'domain': domain})
    return render_to_response("index.html", context)

