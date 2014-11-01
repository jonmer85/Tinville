from django.template.defaulttags import register

@register.filter
def subtract(value, arg):
    return value - arg