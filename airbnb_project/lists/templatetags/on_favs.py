from django import template
from lists import models as list_model

register = template.Library()


@register.simple_tag(takes_context=True)
def on_favs(context, room):
    try:
        user = context.request.user
        the_list = list_model.List.objects.get(user=user, name="My Favorites")
    except list_model.List.DoesNotExist:
        return None

    return room in the_list.rooms.all()
