from django.urls import path

from .views import AccountLoginView, AccountLogoutView, signup

app_name = "accounts"
urlpatterns = [
    path("cadastro/", signup, name="signup"),
    path("entrar/", AccountLoginView.as_view(), name="login"),
    path("sair/", AccountLogoutView.as_view(), name="logout"),
]
