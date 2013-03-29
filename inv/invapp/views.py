from django.shortcuts import get_object_or_404, render

from invapp.models import Collection, Project, Item, Bag, BagAction

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from utils import build_digg_style_boxes


def collection(request, id):
    collection = get_object_or_404(Collection, id=id)
    projects = Project.objects.filter(collection=collection).defer('collection',
        'created')
    items = Item.objects.defer('created', 'original_item_type', 'rawfiles_loc',
        'qcfiles_loc', 'qafiles_loc', 'finfiles_loc', 'ocrfiles_loc',
        'notes').filter(collection=collection)
    if items.count > 10:
        items_paginator = Paginator(items, 10)
        items_page = request.GET.get('items_page')
        try:
            items = items_paginator.page(items_page)
        except PageNotAnInteger:
            items = items_paginator.page(1)
        except EmptyPage:
            items = items_paginator.page(items_paginator.num_pages)
        items.boxes = build_digg_style_boxes(items)
    return render(request, 'collection.html',
        {'collection': collection, 'projects': projects, 'items': items})


def project(request, id):
    project = get_object_or_404(Project, id=id)
    items = Item.objects.defer('collection', 'created', 'original_item_type',
        'rawfiles_loc', 'qcfiles_loc', 'qafiles_loc', 'finfiles_loc',
        'ocrfiles_loc', 'notes').filter(project=project)
    if items.count > 10:
        items_paginator = Paginator(items, 10)
        items_page = request.GET.get('items_page')
        try:
            items = items_paginator.page(items_page)
        except PageNotAnInteger:
            items = items_paginator.page(1)
        except EmptyPage:
            items = items_paginator.page(items_paginator.num_pages)
        items.boxes = build_digg_style_boxes(items)
    return render(request, 'project.html',
        {'project': project, 'items': items})


def item(request, id):
    item = get_object_or_404(Item, id=id)
    bags = Bag.objects.defer('created', 'bag_type', 'payload_raw').filter(item=item)
    return render(request, 'item.html', {'item': item, 'bags': bags})


def bag(request, bagname):
    bag = get_object_or_404(Bag, bagname=bagname)
    actions = BagAction.objects.filter(bag=bag)
    bag_list = bag.payload()
    if bag_list.count > 10:
        bag_paginator = Paginator(bag_list, 10)
        bag_page = request.GET.get('bag_page')
        try:
            bag_list = bag_paginator.page(bag_page)
        except PageNotAnInteger:
            bag_list = bag_paginator.page(1)
        except EmptyPage:
            bag_list = bag_paginator.page(bag_paginator.num_pages)
        bag_list.boxes = build_digg_style_boxes(bag_list)

    return render(request, 'bag.html', {'bag': bag, 'actions': actions, 'bag_list':bag_list})

def home(request):
    collections = Collection.objects.all()
    projects = Project.objects.all()
    items = Item.objects.order_by('created').reverse()[:20]
    return render(request, 'home.html', {'collections': collections,
        'projects': projects, 'items': items})
