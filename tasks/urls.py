from django.urls import path
from tasks import views

urlpatterns = [
    path("", views.TaskListView.as_view(), name="task-list"),
    path("<int:pk>", views.TaskDetailView.as_view(), name="task-detail"),
    path("create-task/", views.TaskCreateView.as_view(), name="task-create"),
    path("<int:pk>/complete/", views.TaskCompleteView.as_view(), name="task-complete")
]
