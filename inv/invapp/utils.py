def build_digg_style_boxes(items):
    tp = items.paginator.num_pages
    # build list of boxes (11 inner boxes + 2 arrows)
    boxes = list(range(13))

    # Add the backward and forward arrows
    boxes[0] = {'disp': '<<', 'link': None, 'disabled': True}
    if items.has_previous():
        boxes[0]['disabled'] = False
        boxes[0]['link'] = str(items.previous_page_number())
    boxes[12] = {'disp': '>>', 'link': None, 'disabled': True}
    if items.has_next():
        boxes[12]['disabled'] = False
        boxes[12]['link'] = str(items.next_page_number())

    # Add the first and last numbers
    boxes[1] = {'disp': '1', 'link': '1'}
    boxes[1]['disabled'] = items.number == 1
    boxes[11] = {'disp': tp, 'link': str(tp)}
    boxes[11]['disabled'] = items.number == tp

    # Add rest of numbers

    # if small, don't bother with left ellipsis
    if items.number < 7:
        for x in range(2, 11):
            boxes[x] = {'disp': str(x), 'link': str(x)}
            boxes[x]['disabled'] = items.number == x
        boxes[10] = {'disp': '...', 'link': None, 'disabled': True}
    # if large, don't bother with right ellipsis
    elif items.number > tp - 6:
        boxes[2] = {'disp': '...', 'link': None, 'disabled': True}
        num = tp - 9
        for x in range(3, 11):
            num += 1
            boxes[x] = {'disp': str(num), 'link': str(num)}
            boxes[x]['disabled'] = items.number == num
    else:
        boxes[2] = {'disp': '...', 'disabled': True}
        for x in range(-3, 4):
            boxes[x+6] = {'disp': str(items.number + x),
                'link': str(items.number + x)}
            boxes[x+6]['disabled'] = x == 0
        boxes[10] = {'disp': '...', 'link': None, 'disabled': True}

    return boxes
