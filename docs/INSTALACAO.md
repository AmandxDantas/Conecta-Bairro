# Instalação e execução local

O projeto requer Python 3.12. Usa Django 5.2, SQLite, templates HTML, CSS e JavaScript; não exige Node.js nem serviços externos.

## Linux e macOS

```bash
git clone https://github.com/AmandxDantas/Conecta-Bairro.git
cd Conecta-Bairro
git switch desenvolvimento
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
# Opcional: carregue .env no shell; SECRET_KEY do exemplo serve apenas para desenvolvimento.
set -a && source .env && set +a
python manage.py migrate
python manage.py seed_categories
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/`. Crie uma conta em **Cadastrar profissional**, conclua o perfil e verifique a busca por categoria e região. Não é necessário criar superusuário para os fluxos públicos; use `python manage.py createsuperuser` somente para administrar cadastros pelo `/admin/`.

## Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py seed_categories
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/`. No Windows, defina variáveis com `$env:SECRET_KEY="uma-chave-local"` e `$env:DEBUG="True"` quando necessário.

## Testes e cobertura

Com o ambiente virtual ativado:

```bash
python manage.py check
coverage run --rcfile=pyproject.toml manage.py test
coverage report --rcfile=pyproject.toml
coverage xml --rcfile=pyproject.toml -o reports/coverage.xml
coverage html --rcfile=pyproject.toml -d reports/coverage-html
coverage report --rcfile=pyproject.toml > reports/coverage.txt
```

Os testes usam o banco temporário isolado criado pelo Django e não inserem nem apagam cadastros da base local. Os relatórios de cobertura são gerados pela execução efetiva da suíte.

## Configuração de publicação

Antes de servir fora da máquina local, configure `SECRET_KEY` forte, `DEBUG=False`, `ALLOWED_HOSTS` com os domínios reais e HTTPS; mantenha `.env` fora do Git. O arquivo SQLite precisa de armazenamento persistente e adequado a escrita. Para operação concorrente ou hospedagem com disco efêmero, adote banco persistente compatível antes de publicar; SQLite local é a configuração solicitada para este projeto acadêmico.
