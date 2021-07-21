from django.urls import path
from . import views

app_name = "lists"

urlpatterns = [
    path("add/<int:room_pk>/", views.toggle_room, name="fav"),
    path("favs/", views.SeeFavsView.as_view(), name="see_fav"),
]
