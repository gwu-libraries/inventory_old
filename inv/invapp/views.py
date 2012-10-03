from django.shortcuts import get_object_or_404, render_to_response

from invapp.models import Collection, Project, Item, Bag


def collection(request, pid):
    collection = get_object_or_404(Collection, pid=pid)
    projects = collection.project_set.all()
    items = collection.item_set.all()
    return render_to_response('collection.html',
        {'collection': collection, 'projects': projects, 'items': items})


def project(request, pid):
    project = get_object_or_404(Project, pid=pid)
    items = project.item_set.all()
    return render_to_response('project.html',
        {'project': project, 'items': items})


def item(request, pid):
    item = get_object_or_404(Item, pid=pid)
    bags = item.bag_set.all()
    return render_to_response('item.html', {'item': item, 'bags': bags})


def bag(request, pid):
    bag = get_object_or_404(Bag, pid=pid)
    return render_to_response('bag.html', {'bag': bag})
