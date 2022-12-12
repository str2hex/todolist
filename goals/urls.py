from django.urls import path
from .view import goals, goalcategory, goalscomments, board

urlpatterns = [
    path('goal_category/create', goalcategory.GoalCategoryCreateView.as_view()),
    path('goal_category/list', goalcategory.GoalCategoryListView.as_view()),
    path("goal_category/<pk>", goalcategory.GoalCategoryView.as_view()),

    path("goal/create", goals.GoalCreateView.as_view()),
    path('goal/list', goals.GoalListView.as_view()),
    path('goal/<pk>', goals.GoalRUDlView.as_view()),

    path('goal_comment/create', goalscomments.GoalCommentsCreateView.as_view()),
    path('goal_comment/list', goalscomments.GoalCommentsListView.as_view()),
    path('goal_comment/<pk>', goalscomments.CommentsRUDView.as_view()),

    path('board/create', board.CreateBoardView.as_view()),
    path('board/list', board.BoardListView.as_view()),
    path('board/<pk>', board.BoardView.as_view()),

]