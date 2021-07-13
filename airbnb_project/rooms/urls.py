from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("create/", views.UploadRoomView.as_view(), name="create_room"),
    path("<int:pk>", views.room_detail, name="detail"),
    path("<int:pk>/edit/", views.EditRoomView.as_view(), name="edit"),
    path("<int:pk>/photos/", views.RoomPhotosView.as_view(), name="photos"),
    path("<int:pk>/photos/add", views.AddPhotoView.as_view(), name="create_photo"),
    path(
        "<int:room_pk>/photos/<int:photo_pk>/delete",
        views.delete_photo,
        name="delete_photo",
    ),
    path(
        "<int:room_pk>/photos/<int:photo_pk>/update",
        views.EditPhotoView.as_view(),
        name="update_photo",
    ),
    path("search/", views.Search, name="search"),
]
