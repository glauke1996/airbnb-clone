from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    # path("create/",views.CreateRoomView.as_views(),name="create"),
    path("<int:pk>", views.room_detail, name="detail"),
    path("<int:pk>/edit", views.EditRoomView.as_view(), name="edit"),
    # path("<int:pk>/photos/", views.RoomPhotosView.as_view(), name="photos"),
    path("search/", views.Search, name="search"),
]
