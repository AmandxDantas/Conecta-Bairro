import re

from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def normalize_whatsapp(value: str) -> str:
    """Retorna somente dígitos e adiciona o código do Brasil quando omitido."""
    digits = re.sub(r"\D", "", value or "")
    if len(digits) in {10, 11}:
        return f"55{digits}"
    return digits


class Category(models.Model):
    name = models.CharField("nome", max_length=80, unique=True)
    slug = models.SlugField("identificador", max_length=90, unique=True, blank=True)
    icon = models.CharField("ícone", max_length=32, default="grid")
    description = models.CharField("descrição", max_length=180, blank=True)
    is_active = models.BooleanField("ativa", default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "categoria"
        verbose_name_plural = "categorias"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Professional(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="professional_profile",
        verbose_name="conta do profissional",
    )
    full_name = models.CharField(
        "nome completo", max_length=120, validators=[MinLengthValidator(3)]
    )
    whatsapp = models.CharField("WhatsApp", max_length=15)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="professionals",
        verbose_name="categoria do serviço",
    )
    neighborhood = models.CharField("bairro", max_length=80)
    city = models.CharField("cidade", max_length=80)
    service_description = models.TextField("descrição dos serviços", max_length=1200)
    is_active = models.BooleanField("perfil publicado", default=True)
    created_at = models.DateTimeField("cadastrado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        ordering = ["full_name"]
        verbose_name = "profissional"
        verbose_name_plural = "profissionais"
        indexes = [
            models.Index(fields=["city", "neighborhood"], name="prof_region_idx"),
            models.Index(fields=["category", "is_active"], name="prof_cat_active_idx"),
        ]

    def __str__(self) -> str:
        return self.full_name

    @property
    def whatsapp_digits(self) -> str:
        return normalize_whatsapp(self.whatsapp)

    @property
    def whatsapp_url(self) -> str:
        return f"https://wa.me/{self.whatsapp_digits}"

    def get_absolute_url(self) -> str:
        return reverse("professionals:detail", kwargs={"pk": self.pk})


class Service(models.Model):
    professional = models.ForeignKey(
        Professional,
        on_delete=models.CASCADE,
        related_name="services",
        verbose_name="profissional",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="services",
        verbose_name="categoria",
    )
    name = models.CharField("nome do serviço", max_length=100)
    description = models.CharField("descrição", max_length=300, blank=True)
    is_active = models.BooleanField("ativo", default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "serviço"
        verbose_name_plural = "serviços"
        constraints = [
            models.UniqueConstraint(
                fields=["professional", "name"], name="unique_professional_service"
            )
        ]

    def __str__(self) -> str:
        return f"{self.name} — {self.professional.full_name}"
