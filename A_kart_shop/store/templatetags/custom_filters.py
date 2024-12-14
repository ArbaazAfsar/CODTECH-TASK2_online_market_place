from django import template

register = template.Library()

@register.filter
def range_filter(value):
    """
    Returns a range object from 0 to the given value (exclusive).
    """
    return range(value)