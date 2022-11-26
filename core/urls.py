from django.urls import path, include

from core.views import CreateUserApiView

urlpatterns = [
    path('core/signup/', CreateUserApiView.as_view()),

]