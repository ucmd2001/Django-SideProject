from django.urls import path
from . import views
from .views import operation,show_events, ajax_login , create_user
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', operation, name='operation'),
    path('operation/', views.operation, name='operation'),
    path('login/', ajax_login, name='ajax_login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create_user/', create_user, name='create_user'),
]