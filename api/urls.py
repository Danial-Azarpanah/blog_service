from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.PostListView.as_view(), name="list"),
    path("post/<str:slug>", views.PostDetailView.as_view(), name="detail"),
    path("add-post", views.PostCreateView.as_view(), name="create"),
]