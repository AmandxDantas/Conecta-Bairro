
import re

from django import forms

from .models import Category, Professional


class ProfessionalForm(forms.ModelForm):
    service_name = forms.CharField(
        label="Nome do serviço principal",
        max_length=100,
        min_length=2,
        help_text="Ex.: Instalação elétrica, faxina residencial ou aula de matemática.",
        widget=forms.TextInput(attrs={"placeholder": "Ex.: Instalação elétrica"}),
    )

    class Meta:
        model = Professional
        fields = [
            "full_name",
            "whatsapp",
            "category",
            "neighborhood",
            "city",
            "service_description",
        ]

        widgets = {
            "full_name": forms.TextInput(attrs={
                "autocomplete": "name",
            }),
            "whatsapp": forms.TextInput(attrs={
                "type": "tel",
                "autocomplete": "tel",
                "inputmode": "tel",
                "placeholder": "(11) 99999-9999",
            }),
            "category": forms.Select(),
            "neighborhood": forms.TextInput(attrs={
                "autocomplete": "address-level3",
            }),
            "city": forms.TextInput(attrs={
                "autocomplete": "address-level2",
            }),
            "service_description": forms.Textarea(attrs={
                "rows": 5,
                "maxlength": 1200,
                "placeholder": "Conte o que você faz, sua experiência e como atende.",
            }),
        }

        labels = {
            "full_name": "Nome completo",
            "whatsapp": "Número de WhatsApp",
            "category": "Categoria do serviço",
            "neighborhood": "Bairro de atendimento",
            "city": "Cidade",
            "service_description": "Descrição dos serviços oferecidos",
        }

        help_texts = {
            "whatsapp": "Inclua DDD. O sistema salva o número em formato internacional.",
            "service_description": "Escreva uma apresentação clara, com até 1.200 caracteres.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(is_active=True)

        if self.instance.pk:
            primary_service = self.instance.services.order_by("pk").first()
            if primary_service:
                self.fields["service_name"].initial = primary_service.name

    def clean_full_name(self):
        name = " ".join(self.cleaned_data["full_name"].split())
        if len(name) < 3 or len(name.split()) < 2:
            raise forms.ValidationError("Informe seu nome e sobrenome.")
        return name

    def clean_whatsapp(self):
        raw = self.cleaned_data["whatsapp"]
        digits = re.sub(r"\D", "", raw)

        if len(digits) not in {10, 11, 12, 13}:
            raise forms.ValidationError("Informe um número válido com DDD (10 ou 11 dígitos).")

        if len(digits) in {12, 13} and not digits.startswith("55"):
            raise forms.ValidationError("Para números internacionais, informe o código 55 do Brasil.")

        if digits.startswith("55") and len(digits) not in {12, 13}:
            raise forms.ValidationError("Após o código 55, informe o DDD e o telefone.")

        return f"+{digits if digits.startswith('55') else '55' + digits}"

    def clean_neighborhood(self):
        return " ".join(self.cleaned_data["neighborhood"].split())

    def clean_city(self):
        return " ".join(self.cleaned_data["city"].split())

    def clean_service_description(self):
        text = self.cleaned_data["service_description"].strip()
        if len(text) < 20:
            raise forms.ValidationError("Descreva seu serviço com pelo menos 20 caracteres.")
        return text


class ProfessionalSearchForm(forms.Form):
    query = forms.CharField(
        label="Que serviço você procura?",
        required=False,
        max_length=100,
        widget=forms.SearchInput(attrs={
            "placeholder": "Ex.: eletricista, faxina, aulas",
            "autocomplete": "off",
        }),
    )

    category = forms.ModelChoiceField(
        label="Categoria",
        queryset=Category.objects.none(),
        required=False,
        empty_label="Todas as categorias",
    )

    region = forms.CharField(
        label="Bairro ou cidade",
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Ex.: Centro, Campinas",
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(is_active=True)
