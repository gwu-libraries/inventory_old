from django import template

register = template.Library()

@register.inclusion_tag('paginator_bar.html')
def bootstrap_paginator_bar(objects, url_key):
    boxes = pagination_boxes(objects, url_key)
    return {'boxes': boxes}


def pagination_boxes(objects, url_key):
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

    tp = objects.paginator.num_pages
    # build list of boxes (11 inner boxes + 2 arrows)
    boxes = list(range(13))

    def link(val):
        return '?%s=%s' % (url_key, val)

    # Add the backward and forward arrows
    boxes[0] = {'disp': '<<', 'link': None, 'disabled': True}
    if objects.has_previous():
        boxes[0]['disabled'] = False
        boxes[0]['link'] = link(objects.previous_page_number())
    boxes[12] = {'disp': '>>', 'link': None, 'disabled': True}
    if objects.has_next():
        boxes[12]['disabled'] = False
        boxes[12]['link'] = link(objects.next_page_number())

    # Add the first and last numbers
    boxes[1] = {'disp': '1', 'link': link(1)}
    boxes[1]['disabled'] = objects.number == 1
    boxes[11] = {'disp': tp, 'link': link(tp)}
    boxes[11]['disabled'] = objects.number == tp

    # Add rest of numbers
    # Always keep at least 3 boxes on either side of the current number
    # -- Unless the current number is less than three away from an edge

    # if small, don't bother with left ellipsis
    if objects.number < 7:
        for x in range(2, 11):
            boxes[x] = {'disp': str(x), 'link': link(x)}
            boxes[x]['disabled'] = objects.number == x
        boxes[10] = {'disp': '...', 'link': None, 'disabled': True}
    # if large, don't bother with right ellipsis
    elif objects.number > tp - 6:
        boxes[2] = {'disp': '...', 'link': None, 'disabled': True}
        num = tp - 9
        for x in range(3, 11):
            num += 1
            boxes[x] = {'disp': str(num), 'link': link(num)}
            boxes[x]['disabled'] = objects.number == num
    else:
        boxes[2] = {'disp': '...', 'link': None, 'disabled': True}
        for x in range(-3, 4):
            boxes[x+6] = {'disp': str(objects.number + x),
                'link': link(objects.number + x)}
            boxes[x+6]['disabled'] = x == 0
        boxes[10] = {'disp': '...', 'link': None, 'disabled': True}

    return boxes