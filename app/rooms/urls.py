from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("list/", views.ListRoomsView.as_view()),
    path("<int:pk>/", views.SeeRoomsView.as_view()), # pk로 적어야 주요키로 인식, 다른 거로 적고 싶으면 view에서 lookup_url_kwarg 설정
    ]
