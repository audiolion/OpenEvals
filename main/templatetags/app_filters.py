from django import template

register = template.Library()

@register.filter(name='convert_100')
def convert_100(value):
    return int(float(value-1)*float(24.75))

@register.filter(name='convert_10')
def convert_10(value):
    return str(round(float(value-1)*float(2.25), 2))

@register.filter(name='color_rate')
def color_rate(value):
    temp = 1;
    if value > 2:
        temp = 2
    if value > 3:
        temp = 3
    if value > 4:
        temp = 4
    return str("color-scale-rate-" + str(temp))