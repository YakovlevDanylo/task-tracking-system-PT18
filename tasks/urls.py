from django.urls import path
from tasks import views

urlpatterns = [
    path("", views.TaskListView.as_view(), name="task-list"),
    path("<int:pk>/", views.TaskDetailView.as_view(), name="task-detail"),
    path("create-task/", views.TaskCreateView.as_view(), name="task-create"),
    path("<int:pk>/complete/", views.TaskCompleteView.as_view(), name="task-complete"),
    path("<int:pk>/update/", views.TaskUpdateView.as_view(), name="task-update"),
    path("<int:pk>/delete/", views.TaskDeleteView.as_view(), name="task-delete"),

    # path for comments
    path("<int:pk>/comment-edit/", views.CommentUpdateView.as_view(), name="comment-edit"),
    path("<int:pk>/comment-delete/", views.CommentDeleteView.as_view(), name="comment-delete"),
]
