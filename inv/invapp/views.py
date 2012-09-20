from django.conf import settings
from django.http import Http404
from invapp import models

def home(request):
    pass

def about(request):
    pass

def robots(request):
    pass

def browse(request, plural_type):
    pass

def create(request, singular_type):
    pass

def read(request, otype, pid):
    thing = models.get(otype.capitalize()).objects.get(pid=pid)
    return render(request, '%s.html' % otype, {otype:otype})

def update(request, singular_type, pid):
    pass

def delete(request, singular_type, pid):
    pass
