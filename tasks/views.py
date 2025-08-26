from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,View
from django.contrib.auth.mixins import LoginRequiredMixin
from tasks.mixins import UserIsOwnerMixin
from tasks import models
from tasks.forms import TaskForm, TaskFilterForm, CommentForm
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied

# Create your views here.
class TaskListView(ListView):
    model = models.Task
    context_object_name = "tasks"
    template_name = "tasks/task_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()

        status = self.request.GET.get("status", "")
        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TaskFilterForm(self.request.GET)
        return context



class TaskDetailView(DetailView):
    model = models.Task
    context_object_name = "task"
    template_name = "tasks/task_detail.html"

    def get_context_data(self, **kwargs):
        content = super().get_context_data()
        content["comment_form"] = CommentForm()
        return content

    def post(self, request, *args, **kwargs):
        print(request.POST)
        task_comment_from = CommentForm(request.POST, request.FILES)

        if task_comment_from.is_valid():
            comment = task_comment_from.save(commit=False)
            comment.author = request.user
            comment.task = self.get_object()
            comment.save()
            return redirect('task-detail', pk=comment.task.pk)
        else:
            print("error")

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = models.Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class TaskCompleteView(UserIsOwnerMixin, View):
    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.status = "complete"
        task.save()
        return HttpResponseRedirect(reverse_lazy('task-list'))

    def get_object(self):
        task_id = self.kwargs.get("pk")
        return get_object_or_404(models.Task, pk=task_id)

class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = models.Task
    form_class = TaskForm
    template_name = "tasks/task_update_form.html"
    success_url = reverse_lazy('task-list')

class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):

    model = models.Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy('task-list')


# View for Comments

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Comment
    form_class = CommentForm
    template_name = "tasks/comment_edit_form.html"

    def form_valid(self, form):
        comment = self.get_object()
        if comment.author != self.request.user:
            raise PermissionDenied("You cannot edit this comment")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('task-detail', kwargs={"pk": self.object.task.pk})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Comment
    template_name = "tasks/comment_delete.html"

    def get_success_url(self):
        return reverse_lazy('task-detail', kwargs={"pk": self.object.task.pk})