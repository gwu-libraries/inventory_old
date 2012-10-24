from django.shortcuts import get_object_or_404, render_to_response

from invapp.models import Collection, Project, Item, Bag, BagAction


def collection(request, pid):
    collection = get_object_or_404(Collection, pid=pid)
    projects = Project.objects.filter(collection=collection)
    items = Item.objects.filter(collection=collection)
    return render_to_response('collection.html',
        {'collection': collection, 'projects': projects, 'items': items})


def project(request, pid):
    project = get_object_or_404(Project, pid=pid)
    items = Item.objects.filter(project=project)
    return render_to_response('project.html',
        {'project': project, 'items': items})


def item(request, pid):
    item = get_object_or_404(Item, pid=pid)
    bags = Bag.objects.filter(item=item)
    return render_to_response('item.html', {'item': item, 'bags': bags})


def bag(request, bagname):
    bag = get_object_or_404(Bag, bagname=bagname)
    actions = BagAction.objects.filter(bag=bag)
    return render_to_response('bag.html', {'bag': bag, 'actions': actions})

def home(request):
    collections = Collection.objects.all()
    projects = Project.objects.all()
    items = Item.objects.all()
    return render_to_response('home.html', {'collections': collections,
        'projects': projects, 'items': items})
