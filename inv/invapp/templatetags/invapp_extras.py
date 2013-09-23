from django import template
from django.utils.safestring import mark_safe

import urllib
import re

register = template.Library()


@register.filter(name='urlize_with_label')
def urlize_with_label(text, arg):
    if re.findall('>.*</a>', text):
        return mark_safe(re.sub(r'>.*</a>', '>' + arg + '</a>', text))
    else:
        return arg


@register.inclusion_tag('paginator_bar.html', takes_context=True)
def bootstrap_paginator_bar(context, objects, url_key):
    boxes = pagination_boxes(context, objects, url_key)
    return {'boxes': boxes}


def pagination_boxes(context, objects, url_key):
    '''Construct a list of dictionaries that represent pagination bar buttons.

    You can then easily loop through the list as you create your html

    Each "button" dictionary contains the following keys:
        'disp' -- the value to display to the user
        'link' -- the value that should be passed to the button's href
        'disabled' -- Boolean to disable current page buttons or next buttons

    url_key is the string value of the key in the url that specifies the page.
        For example, if the url is:
            http://foo.com/collection/bar?items_page=5
        then the url_key is 'items_page'

    objects must be a django Paginator.Page object
        -- or objects must have the follwing attributes:
            paginator.num_pages
            number
        -- and implement the following functions:
            has_previous()
            has_next()
            previous_page_number()
            next_page_number()
    '''

    # get total page count
    tp = objects.paginator.num_pages
    # build list of boxes (11 inner boxes + 2 arrows for most)
    # adjust for lists with less than 11 pages
    size = tp if tp < 11 else 11
    boxes = list(range(size + 2))

    def link(val):
        request = template.resolve_variable('request', context)
        params = request.GET.copy()
        params[url_key] = val
        query_string = urllib.urlencode(params)
        return '?%s' % query_string

    # Add the backward and forward arrows
    boxes[0] = {'disp': '<<', 'link': None, 'disabled': True}
    if objects.has_previous():
        boxes[0]['disabled'] = False
        boxes[0]['link'] = link(objects.previous_page_number())
    boxes[-1] = {'disp': '>>', 'link': None, 'disabled': True}
    if objects.has_next():
        boxes[-1]['disabled'] = False
        boxes[-1]['link'] = link(objects.next_page_number())

    # Add the first and last numbers
    boxes[1] = {'disp': '1', 'link': link(1)}
    boxes[1]['disabled'] = objects.number == 1
    boxes[-2] = {'disp': str(tp), 'link': link(tp)}
    boxes[-2]['disabled'] = objects.number == tp

    # Add rest of numbers
    
    # For small lists, just fill out remaining boxes
    if tp <= 11:
        for x in range(2, tp):
            boxes[x] = {'disp': str(x), 'link': link(x)}
            boxes[x]['disabled'] = objects.number == x

    # For rest: add ellipses to show breaks

    # if near beginning, don't bother with left ellipsis
    elif objects.number < 7:
        for x in range(2, 10):
            boxes[x] = {'disp': str(x), 'link': link(x)}
            boxes[x]['disabled'] = objects.number == x
        boxes[10] = {'disp': '...', 'link': None, 'disabled': True}
    # if near end, don't bother with right ellipsis
    elif objects.number > tp - 6:
        boxes[2] = {'disp': '...', 'link': None, 'disabled': True}
        num = tp - 9
        for x in range(3, 11):
            num += 1
            boxes[x] = {'disp': str(num), 'link': link(num)}
            boxes[x]['disabled'] = objects.number == num
    # otherwise put three pages and ellipsis on both sides of current page
    else:
        boxes[2] = {'disp': '...', 'link': None, 'disabled': True}
        for x in range(-3, 4):
            boxes[x+6] = {'disp': str(objects.number + x),
                'link': link(objects.number + x)}
            boxes[x+6]['disabled'] = x == 0
        boxes[10] = {'disp': '...', 'link': None, 'disabled': True}

    return boxes
