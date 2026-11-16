# Plano de implementação — Conecta Bairro

## Objetivo e decisões

Construir um sistema acadêmico executável localmente com Python 3.12, Django 5.2 e SQLite, mantendo o README do repositório exatamente como fornecido. A branch de trabalho é `desenvolvimento`; `main` não será alterada. A interface será renderizada no servidor por templates Django (HTML5) e complementada com CSS3 e JavaScript sem framework frontend, para manter a instalação simples e adequada ao MVP.

O modelo principal será `Professional`, associado a uma conta Django, a uma categoria e à região (bairro e cidade), com número de WhatsApp e descrição. `Category` alimentará filtros e categorias iniciais; `Service` permitirá relacionar um ou mais serviços a um profissional e categoria sem complicar o formulário do MVP. Consultas serão feitas pelo ORM, com busca combinável por texto, categoria e bairro/cidade. O WhatsApp será apresentado como link `wa.me` com o número normalizado.

A autenticação usará `django.contrib.auth`, `UserCreationForm`/`AuthenticationForm`, sessões Django e o hasher PBKDF2 padrão; o cadastro do profissional exige conta autenticada. Cada perfil é ligado ao usuário proprietário e as rotas de edição usam esse vínculo, nunca um proprietário enviado pelo navegador. Formulários terão validação no servidor, proteção CSRF e escape padrão dos templates. O README existente descreve explicitamente autenticação com hash PBKDF2, o que fundamenta esta escolha funcional para execução independente em ambiente acadêmico/local.

Django 5.2 será fixado em `requirements.txt`; Coverage.py será usado para executar a suíte e produzir relatório textual, XML e HTML real. SQLite será o banco por padrão; `SECRET_KEY`, `DEBUG` e `ALLOWED_HOSTS` serão configuráveis por variáveis de ambiente, com `.env.example` apenas documental. Não será incluído banco de dados com dados pessoais/demo no ZIP. O sistema usará mensagens do Django, paginação, consultas otimizadas com `select_related` e templates acessíveis/responsivos.

## Estrutura do projeto

- `manage.py`: comandos Django.
- `config/`: configurações, URLs globais, WSGI e ASGI.
- `accounts/`: criação de conta, entrada e saída, formulários, URLs e testes de autenticação.
- `professionals/`: categorias, profissionais, serviços, formulários, pesquisa, detalhes, cadastro/edição e comando de carga de categorias; inclui migrações e testes de domínio/integração.
- `templates/`: base visual compartilhada e páginas de início, resultados, perfil, formulários, autenticação e erros.
- `static/css/`, `static/js/`, `static/img/`: identidade visual, comportamento acessível e ícones vetoriais locais.
- `docs/`: instruções de instalação, execução, configuração e publicação local.
- `reports/`: relatórios verdadeiros de cobertura produzidos pela suíte automatizada.
- `.env.example`, `.gitignore`, `requirements.txt`: configuração, exclusões e dependências.
- `manus-routes.json`: manifesto das páginas servido sem fallback HTML para o Preview.

## Design

### Três direções consideradas

- **Caderno cívico contemporâneo (0,04):** editorial acolhedor, azul institucional e acentos de mapa; selecionado.
- **Neo-brutalismo comunitário (0,06):** blocos geométricos de alto contraste e tipografia expressiva.
- **Minimalismo editorial industrial (0,03):** composição técnica, linhas rígidas e azul profundo.

### Direção escolhida: Caderno cívico contemporâneo

- **Movimento:** design cívico contemporâneo, combinando clareza editorial de serviços públicos com calor de uma rede de vizinhança.
- **Princípios centrais:** clareza antes de decoração; proximidade local evidente; ações grandes e previsíveis; acessibilidade como padrão.
- **Filosofia de cor:** azul profundo para confiança, azul médio para ações, branco e azul muito pálido para leitura descansada, e um acento verde-lima discreto para disponibilidade/contato. Contraste será priorizado sobre sutileza.
- **Paradigma de layout:** cabeçalho editorial e faixa de busca larga; conteúdo alinhado à esquerda em fluxo vertical, com filtro lateral em telas amplas e sequência linear no celular; cartões de profissionais em lista informativa, evitando um painel centralizado genérico.
- **Elementos distintivos:** pequenos marcadores de localização inspirados em mapas; etiquetas de categoria com bordas suaves; selo gráfico simples de dois pontos conectados pelo traço de uma rua.
- **Interação:** filtros evidentes e preservados nos resultados; rótulos permanentes nos campos; CTA de WhatsApp destacado e com nome acessível; feedback de sucesso/erro textual, não somente por cor; foco de teclado visível.
- **Animação:** transições curtas de 120–180 ms em foco, hover e abertura de navegação; sem movimento essencial, sem animações contínuas, respeitando `prefers-reduced-motion`.
- **Tipografia:** Manrope para interface e títulos (fallback system-ui), com pesos 400/500/650/750; escala consistente de 0,875rem, 1rem, 1,25rem, 1,75rem e 2,5rem, entrelinha de 1,5 em texto corrido.
- **Essência da marca:** moradores encontram quem resolve perto de casa, sem intermediação — próxima, confiável, prática.
- **Voz da marca:** direta, respeitosa e local. Exemplos: “Um bom profissional pode estar na sua rua.” e “Encontre perto. Combine direto.”
- **Wordmark e símbolo:** nome “Conecta Bairro” em Manrope semibold acompanhado de dois pinos de localização unidos por um caminho curvo; o símbolo será desenhado como SVG local, não texto emoji.
- **Cor proprietária:** azul Conecta `#1769AA`; paleta de apoio `#0E3557`, `#EAF4FB`, `#FFFFFF`, `#167A58` e cinzas frios legíveis.

## Execução e limites

A aplicação servirá templates Django e arquivos estáticos no mesmo processo e porta configurada do projeto. Em produção local, `DEBUG=False`, segredo forte e hosts explícitos serão documentados. O SQLite é apropriado ao escopo acadêmico; qualquer uso com vários processos/alta concorrência requer migração deliberada e persistência de disco. Nenhuma chave/credencial ou conteúdo do `.env` será incluído no controle de versão. O ZIP excluirá `.git`, ambientes virtuais, caches, banco local e temporários, preservando o README original.