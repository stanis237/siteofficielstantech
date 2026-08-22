from django import template

register = template.Library()

@register.filter(name='split')
def split(value, delimiter=','):
    """Split the string by the given delimiter and return a list.
    Example usage in template: {{ "a,b,c"|split:"," }}
    """
    if not isinstance(value, str):
        return []
    return [item.strip() for item in value.split(delimiter)]
