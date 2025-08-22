from django import forms
from tasks.models import Task, Comment

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "status", "priority", "end_time"]

class TaskFilterForm(forms.Form):

    STATUS_CHOICES = [
        ("", "All"),
        ("todo", "TO DO"),
        ("in_progress", "IN PROGRESS"),
        ("complete", "COMPLETE"),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, label="Status")


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"class": "form-control", "placeholder:": "Write your comment here..."}
            )
        }