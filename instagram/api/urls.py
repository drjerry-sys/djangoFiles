from django.urls import path
from .apiviews import UserApiView, UserDetailedApiView

urlpatterns = [
    path('', UserApiView.as_view()),
    path('<int:pk>/', UserDetailedApiView.as_view()),
]