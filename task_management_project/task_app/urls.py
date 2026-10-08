from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # REST APIs urls
    path("api/register/", views.RegisterView.as_view()),
    path("api/login/", views.LoginView.as_view()),
    path("api/logout/", views.LogoutView.as_view()),
    path("api/tasks/", views.TaskListCreateView.as_view()),
    path("api/tasks/<int:pk>/", views.TaskDetailView.as_view()),

    # Frontend pages
    path("", TemplateView.as_view(template_name="login.html")),
    path("register/", TemplateView.as_view(template_name="register.html")),
    path("dashboard/", TemplateView.as_view(template_name="dashboard.html")),
    path("task-form/", TemplateView.as_view(template_name="task_form.html")),
    path("task-detail/", TemplateView.as_view(template_name="task_detail.html")),
]