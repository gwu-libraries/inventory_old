from django.shortcuts import get_object_or_404, render, redirect

from invapp.models import Collection, Project, Item, Bag, BagAction, Machine

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.views import password_change

from django.core.urlresolvers import reverse

from django.utils import simplejson

from django.http import HttpResponse


@login_required
def collection(request, id):
    collection = get_object_or_404(Collection, id=id)
    projects = Project.objects.filter(collection=collection).defer('collection',
                                                                   'created')
    item_name = request.GET.get('search_collection_items')
    if item_name:
        items = Item.objects.defer('created', 'original_item_type',
                                   'notes').filter(collection=collection, title__icontains=item_name)
    else:
        items = Item.objects.defer('created', 'original_item_type',
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
                  {'collection': collection, 'projects': projects,
                      'items': items})


@login_required
def project(request, id):
    project = get_object_or_404(Project, id=id)
    items = Item.objects.defer('collection', 'created', 'original_item_type',
                               'notes').filter(project=project)
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


@login_required
def machine(request, id):
    machine = get_object_or_404(Machine, id=id)
    bags = Bag.objects.filter(machine=machine)
    return render(request, 'machine.html', {'machine': machine, 'bags': bags})


@login_required
def item(request, id):
    item = get_object_or_404(Item, id=id)
    bags = Bag.objects.defer('created', 'bag_type',
        'payload').filter(item=item)
    return render(request, 'item.html', {'item': item, 'bags': bags})


@login_required
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
    return render(request, 'bag.html', {'bag': bag, 'actions': actions,
        'files': files})


@login_required
def home(request):

    search_collection = request.GET.get("search_collection")
    if search_collection:
        collections = Collection.objects.filter(name__icontains=search_collection)
    else:
        collections = Collection.objects.all()

    if collections.count > 10:
        collections_paginator = Paginator(collections, 10)
        collections_page = request.GET.get('collections_page')
        try:
            collections = collections_paginator.page(collections_page)
        except PageNotAnInteger:
            collections = collections_paginator.page(1)
        except EmptyPage:
            collections = collections_paginator.page(collections_paginator.num_pages)

    machines = Machine.objects.all()
    projects = Project.objects.all()
    items = Item.objects.order_by('created').reverse()[:20]
    return render(request, 'home.html', {'collections': collections,
        'projects': projects, 'items': items, 'machines': machines})


def login_user(request):
    def error(message):
        form = AuthenticationForm(None, request.POST)
        return render(request, 'login.html', {'message': message, 'form': form,
                      'next': request.POST.get('next')})

    message = ''
    username = password = ''
    if request.user.is_authenticated():
        return redirect('home')

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next = request.POST.get('next')
                if next:
                    return redirect(next)
                return redirect('home')
            else:
                message = 'Your account is not active, please contact the' + \
                    ' site administrator.'
                return error(message)
        else:
            message = 'Invalid username/password. Please try again!'
            return error(message)
    else:
        form = AuthenticationForm(None, request.POST)
        return render(request, 'login.html', {'message': message, 'form': form,
                      'next': request.GET.get('next')})


def logout_user(request):
    logout(request)
    form = AuthenticationForm(None, request.POST)
    message = 'You have been logged out successfully!'
    return render(request, 'login.html', {'message': message, 'form': form})


@login_required
def change_password(request):
    return password_change(request, template_name='change_password.html',
        post_change_redirect=reverse('change_password_done'))


@login_required
def change_password_done(request):
    messages.success(request, 'Password changed successfully!')
    return redirect('home')


def collection_items_autocomplete(request):
    item_name = request.GET.get('term')
    collection = request.GET.get('collection')
    result = []
    if item_name:
        data = Item.objects.filter(collection=collection, title__icontains=item_name)
        result = simplejson.dumps([o.title for o in data])
    return HttpResponse(result, 'application/json')


def search_collection_autocomplete(request):
    search_collection = request.GET.get('term')
    result = []
    if search_collection:
        data = Collection.objects.filter(name__icontains=search_collection)
        result = simplejson.dumps([o.name for o in data])
    return HttpResponse(result, 'application/json')
