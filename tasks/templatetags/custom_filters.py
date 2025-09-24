from django import template

register = template.Library()

@register.filter
def average(queryset, field_name):
    """
    Calcula el promedio de un campo numérico en una lista o queryset.
    """
    try:
        values = [getattr(obj, field_name) for obj in queryset if getattr(obj, field_name) is not None]
        return sum(values) / len(values) if values else 0
    except (AttributeError, TypeError):
        return 0