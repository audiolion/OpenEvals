from django import template

register = template.Library()

@register.filter(name='convert_100')
def convert_100(value):
    return int(float(value-1)*float(24.75))

@register.filter(name='convert_10')
def convert_10(value):
    return str(round(float(value-1)*float(2.25), 2))