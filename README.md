# Conecta Bairro

Projeto em desenvolvimento.

Plataforma web que aproxima **moradores** e **profissionais autônomos** da mesma comunidade, facilitando a divulgação de serviços locais e a busca por prestadores próximos.

> **Status do projeto:** MVP em fase de planejamento e prototipação (Projeto de Software – Experiência Prática , curso de Análise e Desenvolvimento de Sistemas).

---

## Sobre o projeto

O **Conecta Bairro** permite que profissionais autônomos (como motoboys, eletricistas, diaristas, pintores e jardineiros) cadastrem seus serviços e que moradores encontrem esses profissionais por **categoria** e **região**, entrando em contato direto pelo **WhatsApp**, sem intermediação, taxas ou etapas complexas de contratação.

## Problema e público-alvo

**Problema:** pequenos prestadores de serviço da comunidade têm dificuldade em divulgar seu trabalho e conquistar novos clientes, enquanto moradores têm dificuldade em localizar profissionais próximos e confiáveis.

**Público-alvo:**

| Perfil | Necessidade |
|---|---|
| Profissionais autônomos | Divulgar serviços, apresentar contato e alcançar novos clientes |
| Moradores | Encontrar rapidamente profissionais próximos para serviços domésticos, reparos e manutenção |

## Funcionalidades do MVP

| ID | Requisito | Prioridade |
|---|---|---|
| RF01 | Cadastro de profissionais autônomos (nome, telefone, WhatsApp, bairro e cidade obrigatórios) | Obrigatório |
| RF02 | Cadastro de serviços vinculados a um profissional e a uma categoria | Obrigatório |
| RF03 | Busca de profissionais por categoria e região (bairro/cidade) | Obrigatório |
| RF04 | Visualização do perfil e contato direto via WhatsApp | Obrigatório |
| RF05 | Edição das informações cadastrais pelo próprio profissional | Desejável |

**Ordem de implementação recomendada:** RF01 → RF02 → RF03 → RF04 → RF05.

## Fora do escopo inicial

Para manter o MVP simples e validável, **não** fazem parte da primeira versão:

- Sistema próprio de pagamentos
- Chat interno
- Geolocalização em tempo real
- Agendamento automatizado
- Gestão financeira
- Avaliações e notas dos profissionais
- Mecanismos avançados de recomendação

## Requisitos

### Não funcionais

| ID | Requisito | Resumo |
|---|---|---|
| RNF01 | Autenticação e hash robusto | Login para profissionais; senhas com PBKDF2 + SHA-256 (padrão do Django); nunca em texto limpo, MD5 ou SHA-1 |
| RNF02 | Proteção de dados (OWASP) | Validação de entradas, controle de acesso e consultas seguras via ORM |
| RNF03 | Desempenho e portabilidade | Página de busca carrega em **até 3 s** (celular com 4 GB de RAM, 4G ~10 Mbps, até 20 profissionais) |
| RNF04 | Acessibilidade | Interface acessível e responsiva (detalhes na seção [Acessibilidade](#acessibilidade)) |

### Verificação de desempenho (RNF03)

1. Cadastrar 20 profissionais fictícios em diferentes categorias e bairros.
2. Abrir a página de busca uma vez para aquecimento e depois mais cinco vezes, no mesmo dispositivo, navegador e condição de rede simulada.
3. Registrar os tempos e calcular a **mediana**.
4. Aprovado se a mediana for **≤ 3 segundos**.

## Arquitetura

Arquitetura **monolítica em camadas**, seguindo o padrão **MVC** (no Django, equivalente a MTV):

| Camada | Responsabilidade |
|---|---|
| **Model** | Persistência e consulta dos dados (profissionais, serviços, categorias e regiões) |
| **View** | Telas utilizadas por moradores e profissionais |
| **Controller** | Recebe ações do usuário, valida dados, executa regras e consulta o banco |

### Fluxo principal: busca de profissionais

1. O morador acessa a plataforma e seleciona uma categoria e uma região.
2. A interface envia a busca ao controlador.
3. O controlador valida os dados e consulta o banco.
4. O banco retorna os profissionais correspondentes.
5. O controlador organiza os resultados e os envia à interface.
6. O morador visualiza a lista, abre o perfil e inicia o contato pelo botão de WhatsApp.

## Tecnologias

| Tecnologia | Versão prevista | Função |
|---|---|---|
| Python | 3.12 | Linguagem principal |
| Django | 5.2 LTS | Framework web: rotas, formulários, autenticação e ORM |
| SQLite | – | Banco de dados local para o MVP |
| HTML5 / CSS3 | – | Estrutura e estilo das páginas |
| Bootstrap | 5.3 | Componentes visuais e responsividade |
| JavaScript | ES6+ | Interatividade em formulários e botões |
| Git / GitHub | – | Controle de versões |

> **Evolução:** caso a plataforma cresça e receba muitos acessos simultâneos, o SQLite poderá ser substituído por **PostgreSQL**.

## Modelo de dados

```
Profissional (1) ───── (N) Serviço (N) ───── (1) Categoria
```

### Profissional
| Campo | Tipo | Regra |
|---|---|---|
| `id_profissional` | inteiro | PK, autoincremento |
| `nome` | texto | obrigatório |
| `telefone` | texto | obrigatório |
| `whatsapp` | texto | obrigatório |
| `descricao` | texto | opcional |
| `bairro` | texto | obrigatório |
| `cidade` | texto | obrigatório |

### Categoria
| Campo | Tipo | Regra |
|---|---|---|
| `id_categoria` | inteiro | PK, autoincremento |
| `nome_categoria` | texto | obrigatório e único |
| `descricao` | texto | opcional |

### Serviço
| Campo | Tipo | Regra |
|---|---|---|
| `id_servico` | inteiro | PK, autoincremento |
| `nome_servico` | texto | obrigatório |
| `descricao` | texto | opcional |
| `id_profissional` | inteiro | FK → Profissional |
| `id_categoria` | inteiro | FK → Categoria |

**Minimização de dados:** o sistema não solicita CPF dos moradores, pois não é necessário para buscar profissionais ou iniciar contato. O WhatsApp do profissional é o único dado de contato indispensável ao fluxo.

## Segurança

Controles previstos, alinhados ao **OWASP Top 10**:

| Ameaça | Controle preventivo | Como verificar |
|---|---|---|
| Injeção de SQL | Django ORM, validação no servidor, sem SQL montado com dados do usuário | Testar entradas inválidas e verificar que os registros não são alterados |
| XSS | Escape automático dos templates Django, validação de dados e CSP quando viável | Inserir caracteres especiais e confirmar que aparecem como texto |
| Acesso não autorizado | Autenticação e permissões do Django; cada profissional altera apenas seus dados | Tentar acessar operações restritas sem login ou editar cadastro de outro profissional |
| Exposição de senhas e segredos | Hash seguro do Django, chaves fora do código, HTTPS | Inspecionar o banco e o repositório |
| Configuração insegura / dependências desatualizadas | `DEBUG=False` em produção, dependências atualizadas, mínimo de recursos | Revisar configurações e versões antes da implantação |

Boas práticas adicionais: sessões e logout do Django, proteção contra tentativas repetidas de login e configurações sensíveis em **variáveis de ambiente**.

## Acessibilidade

Requisito **RNF04**, aplicado às três telas principais:

- Botões e áreas de toque com no mínimo **44 × 44 px**
- Contraste adequado entre texto e fundo
- Campos de formulário com **rótulos persistentes**
- Navegação por teclado com **foco visível**
- Layout responsivo (celulares e computadores)
- Mensagens de erro que indicam o problema e como corrigi-lo, sem depender apenas de cor

## Instalação e execução

> As instruções abaixo seguem o fluxo padrão de um projeto Django e devem ser ajustadas conforme a estrutura final do repositório.

**Pré-requisitos:** Python 3.12 e Git.

```bash
# 1. Clonar o repositório
git clone https://github.com/<seu-usuario>/conecta-bairro.git
cd conecta-bairro

# 2. Criar e ativar o ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Configurar variáveis de ambiente (exemplo)
export SECRET_KEY="sua-chave-secreta"
export DEBUG="True"

# 5. Aplicar as migrações
python manage.py migrate

# 6. (Opcional) Criar um superusuário
python manage.py createsuperuser

# 7. Iniciar o servidor de desenvolvimento
python manage.py runserver
```

Acesse em: <http://127.0.0.1:8000/>

### Implantação

Use uma hospedagem compatível com Python/Django que ofereça **HTTPS** e **armazenamento persistente** (necessário para o arquivo SQLite). Em planos gratuitos, observe limites de armazenamento, memória, processamento e períodos de suspensão. Mantenha `DEBUG=False` e os segredos em variáveis de ambiente.

## Estrutura sugerida do projeto

```
conecta-bairro/
├── manage.py
├── requirements.txt
├── README.md
├── conecta_bairro/          # configurações do projeto Django
│   ├── settings.py
│   └── urls.py
└── servicos/                # app principal
    ├── models.py            # Profissional, Categoria, Serviço
    ├── views.py             # busca, cadastro e perfil
    ├── forms.py
    ├── urls.py
    ├── templates/servicos/
    └── static/servicos/
```

## Testes e validação

Teste de usabilidade planejado com **representante externo** (cenário simulado), presencial, em smartphone, com duração de 15 a 20 minutos e apenas **dados fictícios**.

**Tarefas observáveis:**

1. Localizar a opção de cadastro de profissional na tela inicial.
2. Preencher o cadastro de um profissional fictício.
3. Interpretar os resultados da busca e localizar o botão de WhatsApp.

**Critérios de aceitação:**

| Dimensão | Meta |
|---|---|
| Usabilidade | 100% de sucesso (3 de 3 tarefas, sem ajuda) |
| Eficiência | Até 5 minutos por tarefa |
| Satisfação | Nota mínima 4 em escala de 1 (muito difícil) a 5 (muito fácil) |

**Decisão:** *Aceito para implementação*, *Aceito com ajustes* ou *Não aceito*, conforme falhas críticas e dificuldades observadas. Em caso de resultados divergentes, acessibilidade e compreensão têm prioridade sobre o tempo.

## Soluções semelhantes e diferencial

| Plataforma | Pontos fortes | Limitações observadas |
|---|---|---|
| [GetNinjas](https://www.getninjas.com.br/) | Categorias de serviços, orçamentos, aproximação por região | Profissionais usam moedas para liberar contatos, o que pode ser uma barreira financeira |
| [Triider](https://www.triider.com.br/) | Avaliações, chat, agendamento e pagamento integrados | Muitas etapas e funcionalidades, o que aumenta a complexidade de uso |

**Diferencial do Conecta Bairro:** foco em profissionais **da própria comunidade**, busca simples por categoria e localização, perfil com contato direto por **WhatsApp** e **sem custo de liberação de contatos**.

> As análises são documentais e não representam teste prático dos aplicativos. Confirme as regras comerciais diretamente nos sites, pois podem mudar.

## Impacto social e ODS

- **ODS 8 – Trabalho Decente e Crescimento Econômico** (Meta 8.3): amplia a visibilidade de profissionais autônomos e apoia o empreendedorismo local.
- **ODS 11 – Cidades e Comunidades Sustentáveis:** fortalece conexões e serviços na comunidade.

A contribuição é local: aumentar a visibilidade dos profissionais, sem garantir contratações ou renda.

**Indicadores do MVP:**

1. Quantidade de profissionais cadastrados.
2. Quantidade de contatos iniciados pelos moradores (cliques no botão de WhatsApp).

## Roadmap

- [x] Levantamento do problema e público-alvo
- [x] Definição de requisitos, arquitetura e modelo de dados
- [x] Protótipo das telas principais
- [ ] Implementação do MVP (RF01 a RF04)
- [ ] Validação com usuários e coleta de feedback
- [ ] Edição de cadastro (RF05)
- [ ] Avaliações de profissionais
- [ ] Migração para PostgreSQL, se necessário

## Autoria

**Amanda Dantas Araujo Santos**
Tecnologia em Análise e Desenvolvimento de Sistemas 
Projeto de Software 

---

Projeto desenvolvido para fins acadêmicos.
