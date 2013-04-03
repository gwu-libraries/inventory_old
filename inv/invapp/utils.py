def merge_dicts(d1, d2):
    '''
    Combines values within two dictionaries.
    Primarily for use with multi-level dictionaries containing int values.
    Designed for use with file count and size data stored in JSON.
    '''
    for key in d1.keys():
        if isinstance(d1[key], dict):
            merge_dicts(d1[key], d2[key])
        else:
            d1[key] += d2[key]
    return d1


def compare_dicts(d1, d2):
    '''
    Performs a deep level comparison of keys and values within two dicts.
    Returns False if any differences found
    '''
    if set(d1.keys()) - set(d2.keys()) or set(d2.keys()) - set(d1.keys()):
        return False
    for k in d1.keys():
        if isinstance(d1[k], dict):
            if not compare_dicts(d1[k], d2[k]):
                return False
        elif d1[k] != d2[k]:
            return False
    return True


def update_object_stats(model=None, id=None, obj=None):
    # pass model AND id, OR just pass object itself
    if not obj:
        obj = model.objects.get(id=id)
    obj.stats = obj.collect_stats()
    obj.save()


def update_model_stats(model):
    errors = reduce(lambda x,y: x + y,
        map(update_object_stats, model.objects.all()))
    return errors


def update_all_stats():
    from invapp.models import Item, Project, Collection
    errors = reduce(lambda x,y: x + y,
        map(update_model_stats, [Item, Project, Collection]))
    return errors