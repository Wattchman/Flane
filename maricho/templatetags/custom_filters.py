import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name="bold_subheadings")
def bold_subheadings(value):
    """
    Automatically makes subheadings bold. Detects lines that start with ## and wraps them in <strong> tags.
    """
    pattern = r"(?m)^(##\s*)(.*)"
    formatted_text = re.sub(pattern, r"<strong>\2</strong>", value)
    return mark_safe(formatted_text)
register = template.Library()

@register.filter
def range_filter(end):
    return range(end)
