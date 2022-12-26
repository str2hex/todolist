from django.urls import path
from .view import goals, goalcategory, goalscomments, board

urlpatterns = [
    path('goal_category/create', goalcategory.GoalCategoryCreateView.as_view(), name='category_create'),
    path('goal_category/list', goalcategory.GoalCategoryListView.as_view(), name='goal_category_list'),
    path("goal_category/<pk>", goalcategory.GoalCategoryView.as_view(), name='goal_category_update'),

    path("goal/create", goals.GoalCreateView.as_view(), name='goal_create'),
    path('goal/list', goals.GoalListView.as_view(), name='goal_list'),
    path('goal/<pk>', goals.GoalRUDlView.as_view(), name='goal_update'),

    path('goal_comment/create', goalscomments.GoalCommentsCreateView.as_view(), name='goal_comment_create'),
    path('goal_comment/list', goalscomments.GoalCommentsListView.as_view(), name='goal_comment_list'),
    path('goal_comment/<pk>', goalscomments.CommentsRUDView.as_view(), name='goal_comment_update'),

    path('board/create', board.CreateBoardView.as_view(), name='board_create'),
    path('board/list', board.BoardListView.as_view(), name='board_list'),
    path('board/<pk>', board.BoardView.as_view(), name='board_update'),

]