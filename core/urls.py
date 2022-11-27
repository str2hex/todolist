from django.urls import path, include

from . import views

urlpatterns = [
    path('signup', views.CreateUserApiView.as_view(), name='signup'),
    path('login', views.LoginUserView.as_view(), name='login'),
    path('profile', views.LoginUserView.as_view(), name='profile'),

]