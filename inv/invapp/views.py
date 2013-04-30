from django.shortcuts import get_object_or_404, render

from invapp.models import Collection, Project, Item, Bag, BagAction

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json

from django.http import HttpResponse


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
    return render(request, 'project.html',
        {'project': project, 'items': items})


def item(request, id):
    item = get_object_or_404(Item, id=id)
    bags = Bag.objects.defer('created', 'bag_type', 'payload').filter(item=item)
    return render(request, 'item.html', {'item': item, 'bags': bags})


def bag(request, bagname):
    bag = get_object_or_404(Bag, bagname=bagname)
    actions = BagAction.objects.filter(bag=bag)
    files = bag.list_payload()
    file_type = request.GET.get('file_type')
    file_name = request.GET.get('search_bag_files')
    if file_name:
        files = [f for f in files if file_name.lower() in f[0].lower()]

    if file_type and file_type != 'all':
        temp_files = list()
        for f in files:
            ftype = f[0].split('.')[-1].lower()
            if ftype == file_type:
                temp_files.append(f)
        files = temp_files

    if files.count > 10:
        bag_paginator = Paginator(files, 10)
        files_page = request.GET.get('files_page')
        try:
            files = bag_paginator.page(files_page)
        except PageNotAnInteger:
            files = bag_paginator.page(1)
        except EmptyPage:
            files = bag_paginator.page(bag_paginator.num_pages)
    return render(request, 'bag.html', {'bag': bag, 'actions': actions, 'files': files})

# Handles AJAX request for search autocomplete funtionality of Bag file listings
def get_bag_file(request):
    result = []
    file_name = request.GET.get('term', '')
    bag = get_object_or_404(Bag, bagname=request.GET.get('bag_name', ''))
    for file in bag.payload():
        if file_name.lower() in file[0].lower():
            result.append(file[0])

        data = json.dumps(result)

    return HttpResponse(data, 'application/json')


def home(request):
    collections = Collection.objects.all()
    projects = Project.objects.all()
    items = Item.objects.order_by('created').reverse()[:20]
    return render(request, 'home.html', {'collections': collections,
        'projects': projects, 'items': items})
