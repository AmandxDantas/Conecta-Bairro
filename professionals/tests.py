from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from accounts.forms import SignUpForm

from .forms import ProfessionalForm
from .models import Category, Professional, Service, normalize_whatsapp


class ProfessionalFormTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Reformas e reparos", slug="reformas", icon="toolbox")
        self.valid_data = {
            "full_name": "Marina Oliveira",
            "whatsapp": "(11) 99999-1234",
            "category": self.category.pk,
            "neighborhood": "  Vila Nova  ",
            "city": "São Paulo",
            "service_name": "Instalação elétrica",
            "service_description": "Instalações residenciais, manutenção preventiva e pequenos reparos elétricos.",
        }

    def test_valid_form_normalizes_name_region_and_phone(self):
        form = ProfessionalForm(data=self.valid_data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["full_name"], "Marina Oliveira")
        self.assertEqual(form.cleaned_data["neighborhood"], "Vila Nova")
        self.assertEqual(form.cleaned_data["whatsapp"], "+5511999991234")

    def test_required_fields_are_validated(self):
        form = ProfessionalForm(data={})
        self.assertFalse(form.is_valid())
        for field in ("full_name", "whatsapp", "category", "neighborhood", "city", "service_name", "service_description"):
            self.assertIn(field, form.errors)

    def test_rejects_invalid_whatsapp_and_short_description(self):
        data = {**self.valid_data, "whatsapp": "123", "service_description": "Sou eletricista."}
        form = ProfessionalForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("whatsapp", form.errors)
        self.assertIn("service_description", form.errors)

    def test_requires_full_name_with_two_parts(self):
        form = ProfessionalForm(data={**self.valid_data, "full_name": "Marina"})
        self.assertFalse(form.is_valid())
        self.assertIn("full_name", form.errors)

    def test_normalize_whatsapp_helper(self):
        self.assertEqual(normalize_whatsapp("(11) 98765-4321"), "5511987654321")
        self.assertEqual(normalize_whatsapp("+55 11 98765-4321"), "5511987654321")


class CategorySeedCommandTests(TestCase):
    def test_seed_command_creates_twelve_categories_and_is_idempotent(self):
        call_command("seed_categories", verbosity=0)
        self.assertEqual(Category.objects.count(), 12)
        call_command("seed_categories", verbosity=0)
        self.assertEqual(Category.objects.count(), 12)


class AccountFlowTests(TestCase):
    def test_signup_page_and_successful_account_creation(self):
        response = self.client.get(reverse("accounts:signup"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "username": "amanda_local",
                "first_name": "Amanda",
                "last_name": "Santos",
                "email": "amanda@example.com",
                "password1": "UmaSenhaForte2026!",
                "password2": "UmaSenhaForte2026!",
                "next": reverse("professionals:register"),
            },
        )
        self.assertRedirects(response, reverse("professionals:register"))
        user = User.objects.get(username="amanda_local")
        self.assertNotEqual(user.password, "UmaSenhaForte2026!")
        self.assertTrue(user.password.startswith("pbkdf2_sha256$"))
        self.assertIn("_auth_user_id", self.client.session)

    def test_duplicate_email_is_rejected(self):
        User.objects.create_user("existing", email="same@example.com", password="A_forte_Senha_2026!")
        form = SignUpForm(
            data={
                "username": "another",
                "first_name": "Ana",
                "last_name": "Silva",
                "email": "SAME@example.com",
                "password1": "UmaSenhaForte2026!",
                "password2": "UmaSenhaForte2026!",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_login_logout_and_restricted_page(self):
        user = User.objects.create_user("prestadora", password="UmaSenhaForte2026!")
        response = self.client.get(reverse("professionals:register"))
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('professionals:register')}")
        response = self.client.post(reverse("accounts:login"), {"username": "prestadora", "password": "UmaSenhaForte2026!"})
        self.assertRedirects(response, reverse("professionals:home"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)
        response = self.client.post(reverse("accounts:logout"))
        self.assertRedirects(response, reverse("professionals:home"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_signup_does_not_allow_external_redirect(self):
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "username": "safeuser",
                "first_name": "João",
                "last_name": "Souza",
                "email": "joao@example.com",
                "password1": "UmaSenhaForte2026!",
                "password2": "UmaSenhaForte2026!",
                "next": "https://evil.example/",
            },
        )
        self.assertRedirects(response, reverse("professionals:register"))


class ProfessionalDirectoryIntegrationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.electrical = Category.objects.create(name="Reformas e reparos", slug="reformas", icon="toolbox")
        cls.cleaning = Category.objects.create(name="Limpeza", slug="limpeza", icon="broom")
        cls.owner = User.objects.create_user("marina", password="UmaSenhaForte2026!")
        cls.other_user = User.objects.create_user("ricardo", password="UmaSenhaForte2026!")
        cls.professional = Professional.objects.create(
            user=cls.owner,
            full_name="Marina Oliveira",
            whatsapp="+5511999991234",
            category=cls.electrical,
            neighborhood="Vila Nova",
            city="São Paulo",
            service_description="Instalações residenciais e manutenção elétrica com atendimento no bairro.",
        )
        Service.objects.create(
            professional=cls.professional,
            category=cls.electrical,
            name="Instalação elétrica",
            description="Instalação e manutenção.",
        )

    def test_home_displays_identity_and_categories(self):
        response = self.client.get(reverse("professionals:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Conecta")
        self.assertContains(response, "Reformas e reparos")
        self.assertContains(response, "Limpeza")
        self.assertContains(response, "Cadastrar profissional")

    def test_search_filters_by_category_and_region_together(self):
        second_owner = User.objects.create_user("ana", password="UmaSenhaForte2026!")
        Professional.objects.create(
            user=second_owner,
            full_name="Ana Costa",
            whatsapp="+5511987654321",
            category=self.cleaning,
            neighborhood="Centro",
            city="Campinas",
            service_description="Limpeza residencial detalhada, organização e faxina semanal para famílias.",
        )
        response = self.client.get(
            reverse("professionals:search"),
            {"category": self.electrical.pk, "region": "vila"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Marina Oliveira")
        self.assertNotContains(response, "Ana Costa")
        self.assertContains(response, "Vila Nova, São Paulo")

    def test_search_matches_service_text_and_shows_empty_state(self):
        response = self.client.get(reverse("professionals:search"), {"query": "instalação elétrica"})
        self.assertContains(response, "Marina Oliveira")
        self.assertContains(response, "wa.me/5511999991234")
        response = self.client.get(reverse("professionals:search"), {"region": "Bairro distante"})
        self.assertContains(response, "Não encontramos profissionais por aqui ainda.")
        self.assertNotContains(response, "Marina Oliveira")

    def test_invalid_category_filter_does_not_reveal_all_professionals(self):
        response = self.client.get(reverse("professionals:search"), {"category": "99999"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Marina Oliveira")
        self.assertContains(response, "Não encontramos profissionais por aqui ainda.")

    def test_inactive_service_is_not_searchable_by_name_or_description(self):
        Service.objects.create(
            professional=self.professional,
            category=self.electrical,
            name="Atendimento pausado",
            description="Disponibilidade suspensa temporariamente.",
            is_active=False,
        )
        for query in ("pausado", "suspensa"):
            response = self.client.get(reverse("professionals:search"), {"query": query})
            self.assertNotContains(response, "Marina Oliveira")

    def test_inactive_service_is_not_shown_on_public_profile(self):
        Service.objects.create(
            professional=self.professional,
            category=self.electrical,
            name="Atendimento pausado",
            description="Disponibilidade suspensa temporariamente.",
            is_active=False,
        )
        response = self.client.get(self.professional.get_absolute_url())
        self.assertContains(response, "Instalação elétrica")
        self.assertNotContains(response, "Atendimento pausado")

    def test_authenticated_registration_creates_profile_and_primary_service(self):
        self.client.force_login(self.other_user)
        response = self.client.post(
            reverse("professionals:register"),
            {
                "full_name": "Ricardo Almeida",
                "whatsapp": "(11) 98888-7777",
                "category": self.electrical.pk,
                "neighborhood": "Jardim Sul",
                "city": "São Paulo",
                "service_name": "Reparo residencial",
                "service_description": "Faço manutenção elétrica, troca de tomadas e pequenos reparos para residências.",
            },
        )
        new_profile = Professional.objects.get(user=self.other_user)
        self.assertRedirects(response, new_profile.get_absolute_url())
        self.assertTrue(Service.objects.filter(professional=new_profile, name="Reparo residencial").exists())
        self.assertEqual(new_profile.whatsapp, "+5511988887777")

    def test_registration_missing_required_fields_shows_actionable_errors(self):
        self.client.force_login(self.other_user)
        response = self.client.post(reverse("professionals:register"), {})
        self.assertEqual(response.status_code, 200)
        self.assertIn("full_name", response.context["form"].errors)
        self.assertIn("service_description", response.context["form"].errors)
        self.assertFalse(Professional.objects.filter(user=self.other_user).exists())

    def test_edit_updates_only_the_authenticated_owners_profile(self):
        self.client.force_login(self.owner)
        response = self.client.post(
            reverse("professionals:edit"),
            {
                "full_name": "Marina Oliveira",
                "whatsapp": "(11) 99999-1234",
                "category": self.cleaning.pk,
                "neighborhood": "Jardim Azul",
                "city": "São Paulo",
                "service_name": "Limpeza residencial",
                "service_description": "Limpeza residencial cuidadosa, organização de ambientes e faxina para casas.",
            },
        )
        self.assertRedirects(response, self.professional.get_absolute_url())
        self.professional.refresh_from_db()
        self.assertEqual(self.professional.neighborhood, "Jardim Azul")
        self.assertEqual(self.professional.category, self.cleaning)
        self.assertEqual(self.professional.services.get().name, "Limpeza residencial")

    def test_user_cannot_edit_another_users_profile(self):
        self.client.force_login(self.other_user)
        response = self.client.get(reverse("professionals:edit"))
        self.assertEqual(response.status_code, 404)
        self.professional.refresh_from_db()
        self.assertEqual(self.professional.full_name, "Marina Oliveira")

    def test_public_profile_contains_direct_whatsapp_contact(self):
        response = self.client.get(self.professional.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Marina Oliveira")
        self.assertContains(response, "Vila Nova, São Paulo")
        self.assertContains(response, "https://wa.me/5511999991234")

    def test_manifest_is_served_as_json_not_html(self):
        response = self.client.get("/manus-routes.json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertIn('"/profissionais/:id/"', response.content.decode())
