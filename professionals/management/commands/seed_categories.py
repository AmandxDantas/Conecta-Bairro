from django.core.management.base import BaseCommand

from professionals.models import Category


CATEGORIES = [
    ("Reformas e reparos", "reformas-e-reparos", "toolbox", "Eletricista, encanador, pintor e pequenos reparos."),
    ("Limpeza", "limpeza", "broom", "Faxina residencial, limpeza pós-obra e organização."),
    ("Beleza e bem-estar", "beleza-e-bem-estar", "sparkles", "Cabelo, maquiagem, massagem e cuidados pessoais."),
    ("Aulas e cursos", "aulas-e-cursos", "book", "Reforço escolar, idiomas, música e outras aulas."),
    ("Tecnologia", "tecnologia", "laptop", "Informática, suporte técnico e instalação de redes."),
    ("Transporte", "transporte", "car", "Fretes, mudanças e transporte local."),
    ("Jardinagem", "jardinagem", "leaf", "Jardins, podas, plantas e manutenção de áreas verdes."),
    ("Pets", "pets", "paw", "Banho, passeio, cuidados e serviços para animais."),
    ("Alimentação", "alimentacao", "utensils", "Comida caseira, bolos e serviços de cozinha."),
    ("Eventos", "eventos", "party", "Fotografia, decoração e apoio para eventos."),
    ("Serviços domésticos", "servicos-domesticos", "home", "Apoio e manutenção para o dia a dia da casa."),
    ("Outros serviços", "outros-servicos", "grid", "Outros serviços oferecidos na comunidade."),
]


class Command(BaseCommand):
    help = "Cria ou atualiza as categorias padrão do Conecta Bairro."

    def handle(self, *args, **options):
        created_count = 0
        for name, slug, icon, description in CATEGORIES:
            _category, created = Category.objects.update_or_create(
                slug=slug,
                defaults={"name": name, "icon": icon, "description": description, "is_active": True},
            )
            created_count += int(created)
        self.stdout.write(
            self.style.SUCCESS(
                f"Categorias prontas: {len(CATEGORIES)} no total, {created_count} criadas agora."
            )
        )
