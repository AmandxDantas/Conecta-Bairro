# Pull Request para `main`

O trabalho foi desenvolvido na branch `desenvolvimento`, criada a partir da branch homônima existente no repositório. A branch `main` não foi alterada. O ambiente desta execução dispõe apenas de leitura pública do repositório; não há sessão autenticada autorizada para enviar a branch ou abrir um Pull Request.

Depois de levar estes arquivos para uma cópia autenticada do repositório (ou habilitar a conexão GitHub autorizada), envie a branch e abra um PR com destino `main`:

```bash
git switch desenvolvimento
git push -u origin desenvolvimento
```

Compare `desenvolvimento` → `main` e revise o diff antes de criar o PR:

<https://github.com/AmandxDantas/Conecta-Bairro/compare/main...desenvolvimento?expand=1>

## Resumo sugerido

- Implementa cadastro/login de contas com o hash PBKDF2 do Django.
- Adiciona diretório de profissionais, perfis, categorias, serviços, filtros por categoria/região e contato direto pelo WhatsApp.
- Protege cadastro/edição e limita edição ao proprietário do perfil.
- Inclui interface responsiva, migrações, comando de carga inicial, instruções e testes automatizados.

## Evidência de validação

`python manage.py check` e verificação de migrações sem alterações pendentes; suíte executada com Coverage.py: 24 testes aprovados, cobertura total medida de 94%. O `README.md` preexistente foi mantido byte a byte.