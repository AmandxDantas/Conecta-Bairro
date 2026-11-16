# Conecta Bairro — instruções rápidas

Para instalação detalhada e execução em Windows/Linux/macOS, consulte [`docs/INSTALACAO.md`](docs/INSTALACAO.md). O projeto utiliza Python 3.12, Django 5.2 e SQLite; não precisa de serviços externos.

Após ativar o ambiente virtual e instalar `requirements.txt`, execute `python manage.py migrate`, `python manage.py seed_categories` e `python manage.py runserver`. Crie uma conta no site e cadastre um perfil para começar a testar a busca.

Para executar os testes e produzir evidências verdadeiras de cobertura: `coverage run --rcfile=pyproject.toml manage.py test`, seguido de `coverage report --rcfile=pyproject.toml`, `coverage xml --rcfile=pyproject.toml -o reports/coverage.xml`, `coverage html --rcfile=pyproject.toml -d reports/coverage-html` e `coverage report --rcfile=pyproject.toml > reports/coverage.txt`.

O arquivo [`README.md`](README.md) preexistente foi preservado sem alterações. Segredos devem ficar em `.env` local (ignorado pelo Git), nunca em commits ou no arquivo `.env.example`.