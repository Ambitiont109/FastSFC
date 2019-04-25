from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


@register.filter(name='size')
def size(value):
    if value == -1:
        return '-'
    return intcomma(value) + ' kb'
