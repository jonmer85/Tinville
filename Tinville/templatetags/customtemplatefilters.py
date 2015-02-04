from django.template.defaulttags import register

@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def addcss(value, arg):
    return value.as_widget(attrs={'class': arg})