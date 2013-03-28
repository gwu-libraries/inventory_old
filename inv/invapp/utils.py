def build_digg_style_boxes(objects, url_key):
    tp = objects.paginator.num_pages
    # build list of boxes (11 inner boxes + 2 arrows)
    boxes = list(range(13))

    def link(val):
        return '?%s=%s' % (url_key, val)

    # Add the backward and forward arrows
    boxes[0] = {'disp': '<<', 'link': None, 'disabled': True}
    if objects.has_previous():
        boxes[0]['disabled'] = False
        boxes[0]['link'] = str(objects.previous_page_number())
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