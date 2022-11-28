from django.urls import path
from . import views

urlpatterns = [
    path('', views.GoalCategoryCreateView.as_view())
]