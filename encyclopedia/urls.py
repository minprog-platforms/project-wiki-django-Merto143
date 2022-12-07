from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("random", views.random_page, name="random"),
    path("new_page", views.new_page, name="new_page"),
    path("<str:title>", views.page, name="page")
    
]
