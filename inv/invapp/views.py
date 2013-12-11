from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import password_change
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect

from invapp.models import Collection, Project, Item, Bag, BagAction, Machine


@login_required
def collection(request, id):
    collection = get_object_or_404(Collection, id=id)
    projects = Project.objects.filter(collection=collection)
    projects = projects.defer('collection', 'created')
    item_name = request.GET.get('search_collection_items')
    items = Item.objects.defer('created', 'original_item_type', 'notes')
    items = items.filter(collection=collection)
    if item_name:
        items = items.filter(Q(id__icontains=item_name) |
                             Q(title__icontains=item_name) |
                             Q(local_id__icontains=item_name))
    items = _paginate(items, request.GET.get('items_page'))
    return render(request, 'collection.html',
                  {'title': 'collection: %s' % collection.name,
                   'collection': collection, 'projects': projects,
                   'items': items})


@login_required
def project(request, id):
    project = get_object_or_404(Project, id=id)

    item_name = request.GET.get('search_project_items')
    if item_name:
        items = Item.objects.defer('created', 'original_item_type',
                                   'notes').filter(project=project).filter(
                                       Q(id__icontains=item_name) |
                                       Q(title__icontains=item_name) |
                                       Q(local_id__icontains=item_name))
    else:
        items = Item.objects.defer('created', 'original_item_type',
                                   'notes').filter(project=project)

    items = _paginate(items, request.GET.get('items_page'))
    return render(request, 'project.html',
                  {'project': project, 'items': items})


@login_required
def machine(request, id):
    machine = get_object_or_404(Machine, id=id)
    bags = Bag.objects.filter(machine=machine)
    bags = _paginate(bags, request.GET.get('bags_page'))
    return render(request, 'machine.html', {'machine': machine, 'bags': bags})


@login_required
def item(request, id):
    item = get_object_or_404(Item, id=id)
    bags = Bag.objects.defer('created', 'bag_type', 'payload')
    bags = bags.filter(item=item)
    actions = BagAction.objects.filter(bag__item=item).order_by('bag__bagname', 'timestamp')
    return render(request, 'item.html', {'title': 'item: %s' % item.title,
                  'item': item, 'bags': bags, 'actions': actions})


@login_required
def bag(request, bag_id):
    bag = get_object_or_404(Bag, id=bag_id)
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
    files = _paginate(files, request.GET.get('files_page'))
    return render(request, 'bag.html', {'title': 'bag: %s' % bag.bagname,
                  'bag': bag, 'actions': actions, 'files': files})


@login_required
def home(request):
    search_collection = request.GET.get("search_collection")
    if search_collection:
        collections = Collection.objects.filter(
            Q(name__icontains=search_collection) |
            Q(local_id__icontains=search_collection) |
            Q(id__icontains=search_collection))
    else:
        collections = Collection.objects.all()

    collections = _paginate(collections, request.GET.get('collections_page'))

    search_project = request.GET.get("search_project")
    if search_project:
        projects = Project.objects.filter(Q(name__icontains=search_project) |
                                          Q(id__icontains=search_project))
    else:
        projects = Project.objects.all()

    projects = _paginate(projects, request.GET.get('project_page'))

    machines = Machine.objects.all()
    items = Item.objects.order_by('created').reverse()[:20]
    return render(request, 'home.html', {'title': 'home',
                  'collections': collections, 'projects': projects,
                  'items': items, 'machines': machines})


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
    item_name = request.GET.get('search')
    collection = request.GET.get('collection')
    result = []
    if item_name:
        data = Item.objects.filter(collection=collection).filter(
            Q(title__icontains=item_name) | Q(id__icontains=item_name) |
            Q(local_id__icontains=item_name))
        result = serializers.serialize('json', data,
                                       fields=('title', 'local_id'))
    return HttpResponse(result, 'application/json')


def search_collection_autocomplete(request):
    search_collection = request.GET.get('search')
    result = []
    if search_collection:
        data = Collection.objects.filter(Q(name__icontains=search_collection) |
                                         Q(local_id__icontains=search_collection) |
                                         Q(id__icontains=search_collection))
        result = serializers.serialize('json', data, fields=('name'))
    return HttpResponse(result, 'application/json')


def search_project_autocomplete(request):
    project = request.GET.get('search')
    result = []
    if project:
        data = Project.objects.filter(Q(name__icontains=project) |
                                      Q(id__icontains=project))
        result = serializers.serialize('json', data, fields=('name'))
    return HttpResponse(result, 'application/json')


def project_items_autocomplete(request):
    item_name = request.GET.get('search')
    project = request.GET.get('project')
    result = []
    if item_name:
        data = Item.objects.filter(project=project).filter(
            Q(title__icontains=item_name) | Q(id__icontains=item_name) |
            Q(local_id__icontains=item_name))
        result = serializers.serialize('json', data,
                                       fields=('title', 'local_id'))
    return HttpResponse(result, 'application/json')


def _paginate(items, page):
    if items.count > 10:
        items_paginator = Paginator(items, 10)
        try:
            items = items_paginator.page(page)
        except PageNotAnInteger:
            items = items_paginator.page(1)
        except EmptyPage:
            items = items_paginator.page(items_paginator.num_pages)
    return items
