from django import template

register = template.Library()


@register.filter(name="sexy_capitals")
def sexy_capitals(value):
    return value.capitalize()
