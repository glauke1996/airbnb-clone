from django.urls import path
from reservations import views

app_name = "reservations"

urlpatterns = [
    path(
        "create/<int:room>/<int:year>-<int:month>-<int:day>/",
        views.CreateReservationView,
        name="create",
    ),
    path("<int:pk>/", views.ReservationDetailView.as_view(), name="detail"),
    path(
        "<int:pk>/<str:verb>",
        views.EditReservationView,
        name="update_reservation",
    ),
    path(
        "list/",
        views.MyReservationView.as_view(),
        name="list",
    ),
]
