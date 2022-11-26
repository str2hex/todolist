from django.urls import path, include

from core.views import CreateUserApiView

urlpatterns = [
    path('signup/', CreateUserApiView.as_view(), name='signup'),

]