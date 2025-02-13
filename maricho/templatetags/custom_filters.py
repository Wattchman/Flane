import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name="bold_subheadings")
def bold_subheadings(value):
    """
    Detects Markdown-style subheadings (## Heading) and makes them bold.
    """
    if not value:
        return ""

    # Pattern to match lines that start with "## " and extract the heading text
    pattern = r"(?m)^##\s*(.+)$"

    # Replace with <strong> HTML tag
    formatted_text = re.sub(pattern, r"<strong>\1</strong>", value)

    return mark_safe(formatted_text)
