from django.urls import path, include

from core.views import CreateUserApiView, LoginUserView

urlpatterns = [
    path('signup', CreateUserApiView.as_view(), name='signup'),
    path('login', LoginUserView.as_view(), name='login'),

]