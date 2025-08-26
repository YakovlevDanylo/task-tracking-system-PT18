from django import template

register = template.Library()

@register.filter(name="endswith")
def endswith(value, ex):
    return value.lower().endswith(ex.lower())