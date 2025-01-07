from django import template
register = template.Library()

@register.filter
def range_filter(end):
    return range(end)