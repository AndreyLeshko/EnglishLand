from django import template


register = template.Library()


@register.filter
def times(number):
    return list(range(1, number+1))
