from django.urls import path

from . import views

app_name = "professionals"
urlpatterns = [
    path("", views.home, name="home"),
    path("buscar/", views.search, name="search"),
    path("profissionais/novo/", views.register, name="register"),
    path("profissionais/editar/", views.edit, name="edit"),
    path("profissionais/<int:pk>/", views.detail, name="detail"),
]
