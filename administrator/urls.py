from django.urls import path
from .views import LoginView, AdminOnlyView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('admin-view/', AdminOnlyView.as_view()),
]
