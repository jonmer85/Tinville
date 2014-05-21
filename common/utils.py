
def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None

def get_list_or_empty(model, **kwargs):
    try:
        return list(model.objects.filter(**kwargs))
    except model.DoesNotExist:
        return []