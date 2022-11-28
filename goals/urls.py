from django.urls import path
from . import views

urlpatterns = [
    path('goal_category/create', views.GoalCategoryCreateView.as_view()),
    path('goal_category/list', views.GoalCategoryListView.as_view()),
]