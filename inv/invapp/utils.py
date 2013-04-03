def merge_dicts(d1, d2):
    '''
    Combines integer values within two multi-level dictionaries.
    Designed for use with file count and size data stored in JSON.
    '''
    # check for keys in d1 not in d2
    for key in set(d1.keys()) - set(d2.keys()):
        d2[key] = {} if isinstance(d1[key], dict) else 0
    # check for keys in d2 not in d1
    for key in set(d2.keys()) - set(d1.keys()):
        d1[key] = {} if isinstance(d2[key], dict) else 0
    # now use recursion to merge subdicts, otherwise add values
    for key in d1:
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


def update_object_stats(obj=None, model=None, id=None):
    # Pass model AND id, OR just pass object itself
    if not obj:
        obj = model.objects.get(id=id)
    obj.stats = obj.collect_stats()
    obj.save()


def update_object_stats_quietly(obj=None, model=None, id=None):
    # Return errors instead of raising them. For use with bulk updating
    try:
        update_object_stats(obj=obj, model=model, id=id)
    except Exception, e:
        if obj:
            id = obj.id
            model = obj.__class__.__name__
        return 'Error updating %s %s: %s' % (model, id, e)


def update_model_stats(model):
    errors = map(update_object_stats_quietly, model.objects.all())
    return [e for e in errors if e]


def update_all_stats():
    from invapp.models import Item, Project, Collection
    return reduce(lambda x,y: x + y,
        map(update_model_stats, [Item, Project, Collection]))