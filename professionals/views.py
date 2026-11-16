from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Prefetch, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProfessionalForm, ProfessionalSearchForm
from .models import Category, Professional, Service


def _sync_primary_service(professional: Professional, service_name: str) -> None:
    service = professional.services.order_by("pk").first()
    if service is None:
        Service.objects.create(
            professional=professional,
            category=professional.category,
            name=service_name,
            description=professional.service_description[:300],
        )
    else:
        service.category = professional.category
        service.name = service_name
        service.description = professional.service_description[:300]
        service.save(update_fields=["category", "name", "description"])


def home(request):
    categories = Category.objects.filter(is_active=True)
    form = ProfessionalSearchForm(request.GET or None)
    return render(request, "professionals/home.html", {"categories": categories, "search_form": form})


def search(request):
    form = ProfessionalSearchForm(request.GET or None)
    professionals = (
        Professional.objects.filter(is_active=True, category__is_active=True)
        .select_related("category", "user")
        .prefetch_related(
            Prefetch("services", queryset=Service.objects.filter(is_active=True))
        )
    )
    if not form.is_valid():
        professionals = professionals.none()
    else:
        query = form.cleaned_data.get("query", "").strip()
        category = form.cleaned_data.get("category")
        region = form.cleaned_data.get("region", "").strip()
        if query:
            professionals = professionals.filter(
                Q(full_name__icontains=query)
                | Q(category__name__icontains=query)
                | Q(service_description__icontains=query)
                | Q(services__is_active=True, services__name__icontains=query)
                | Q(services__is_active=True, services__description__icontains=query)
            )
        if category:
            professionals = professionals.filter(category=category)
        if region:
            professionals = professionals.filter(
                Q(neighborhood__icontains=region) | Q(city__icontains=region)
            )
    professionals = professionals.distinct().order_by("full_name")
    paginator = Paginator(professionals, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "professionals/search.html",
        {"search_form": form, "page_obj": page_obj, "professionals": page_obj.object_list},
    )


@login_required
def register(request):
    try:
        existing = request.user.professional_profile
    except Professional.DoesNotExist:
        existing = None
    if existing:
        messages.info(request, "Você já tem um perfil profissional. Atualize seus dados quando precisar.")
        return redirect("professionals:edit")

    form = ProfessionalForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            professional = form.save(commit=False)
            professional.user = request.user
            professional.save()
            _sync_primary_service(professional, form.cleaned_data["service_name"])
        messages.success(request, "Cadastro concluído! Seu perfil profissional já está disponível para moradores.")
        return redirect(professional.get_absolute_url())
    return render(request, "professionals/professional_form.html", {"form": form, "editing": False})


@login_required
def edit(request):
    try:
        professional = request.user.professional_profile
    except Professional.DoesNotExist as exc:
        raise Http404("Você ainda não possui um perfil profissional.") from exc

    form = ProfessionalForm(
        request.POST if request.method == "POST" else None, instance=professional
    )
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            professional = form.save()
            _sync_primary_service(professional, form.cleaned_data["service_name"])
        messages.success(request, "Seus dados profissionais foram atualizados.")
        return redirect(professional.get_absolute_url())
    return render(request, "professionals/professional_form.html", {"form": form, "editing": True})


def detail(request, pk: int):
    professional = get_object_or_404(
        Professional.objects.select_related("category", "user").prefetch_related(
            Prefetch("services", queryset=Service.objects.filter(is_active=True))
        ),
        pk=pk,
        is_active=True,
    )
    return render(request, "professionals/detail.html", {"professional": professional})
