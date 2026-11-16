from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import SignUpForm


class SignUpFormTests(TestCase):
    def test_signup_form_requires_all_identity_fields(self):
        form = SignUpForm(data={})
        self.assertFalse(form.is_valid())
        for field in ("username", "first_name", "last_name", "email", "password1", "password2"):
            self.assertIn(field, form.errors)

    def test_signup_form_rejects_password_confirmation_mismatch(self):
        form = SignUpForm(
            data={
                "username": "ana",
                "first_name": "Ana",
                "last_name": "Costa",
                "email": "ana@example.com",
                "password1": "UmaSenhaForte2026!",
                "password2": "OutraSenhaForte2026!",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)


class LoginPageTests(TestCase):
    def test_invalid_credentials_do_not_authenticate(self):
        User.objects.create_user("morador", password="UmaSenhaForte2026!")
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "morador", "password": "errada"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertContains(response, "Não foi possível entrar")

    def test_logout_only_accepts_post(self):
        User.objects.create_user("morador", password="UmaSenhaForte2026!")
        self.client.login(username="morador", password="UmaSenhaForte2026!")
        response = self.client.get(reverse("accounts:logout"))
        self.assertEqual(response.status_code, 405)
        self.assertIn("_auth_user_id", self.client.session)
