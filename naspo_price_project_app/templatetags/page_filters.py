from django import template

register = template.Library()

@register.filter
def previous_page(value):
    try: 
        return max(int(value) - 1, 1)
    except (ValueError, TypeError):
        return 1
    
@register.simple_tag
def next_page(value, max_value):
    try:
        return min(int(value) + 1, int(max_value))
    except (ValueError, TypeError):
        return value