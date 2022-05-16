from rest_framework.routers import SimpleRouter
from django.urls import path

from user.views import (
    UserCodeSendView,
    UserRegisterView,
    UserProfileView,
)

urlpatterns = [
    path('send-code/', UserCodeSendView.as_view()),
    path('user-register/', UserRegisterView.as_view()),
    path('user-profile/', UserProfileView.as_view()),
]
