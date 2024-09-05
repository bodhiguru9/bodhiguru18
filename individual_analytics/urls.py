from django.urls import path
from .views import UserListView, UserDetailView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('user/<str:email>/', UserDetailView.as_view(), name='user-detail'),
]