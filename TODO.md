# TODO — Conecta Bairro

## Inicialização e descoberta local
- [x] A tela inicial deve apresentar o nome e a identidade visual Conecta Bairro, campo de pesquisa de serviços, categorias de serviços, botão para entrar e botão para cadastrar profissional. A tela inicial facilita a busca por serviços próximos e diferencia as ações de moradores e profissionais.
- [x] A página inicial mostra as categorias ativas mesmo antes de cada categoria ter profissionais cadastrados; categorias podem ser selecionadas para abrir a pesquisa.

## Cadastro e gestão de profissionais
- [x] O cadastro contém nome completo, número de WhatsApp, categoria do serviço, região de atendimento e descrição dos serviços oferecidos. Inclui também o nome do serviço principal previsto no modelo acadêmico existente.
- [x] O sistema valida no servidor os campos obrigatórios e apresenta mensagem de confirmação após o cadastro.
- [x] Profissionais cadastrados podem editar somente suas próprias informações; o proprietário é atribuído pelo servidor a partir da sessão autenticada e não pode ser escolhido pelo formulário.
- [x] O modelo de dados representa categorias, profissionais e serviços relacionados a um profissional e a uma categoria, conforme a documentação acadêmica preexistente.

## Pesquisa, resultados e contato
- [x] A pesquisa permite procurar profissionais por categoria, nome/descrição/serviço e filtrar por região de atendimento (bairro ou cidade).
- [x] São exibidos profissionais encontrados; parâmetros inválidos não revelam toda a lista; uma mensagem apropriada aparece quando nenhum profissional corresponde à busca.
- [x] Cada resultado mostra nome do profissional, categoria do serviço, bairro/cidade de atendimento e descrição do serviço.
- [x] Cada resultado e perfil público disponibiliza botão de contato direto pelo WhatsApp, com número normalizado para o link wa.me.

## Contas e proteção de acesso
- [x] Há tela de login e fluxo de cadastro/autenticação de usuários com validação de formulário e hash PBKDF2 padrão do Django.
- [x] Cadastro e edição do perfil profissional exigem autenticação; saída é executada via POST.
- [x] A edição é vinculada ao perfil do usuário autenticado e bloqueia acesso de quem não possui perfil; testes confirmam que outro usuário não altera o cadastro.

## Interface e acessibilidade
- [x] A interface é moderna, profissional e intuitiva, com azul e branco como cores principais, botões identificáveis, ícones vetoriais de serviços, campos organizados, textos legíveis e contraste adequado.
- [x] O layout responde a celulares e computadores e mantém uma sequência simples para pessoas com pouca experiência digital.
- [x] A interface inclui alvos de toque de pelo menos 44 × 44 px, rótulos persistentes, navegação por teclado e foco visível, erros textuais explicativos e respeito à preferência de movimento reduzido.

## Estrutura, operação e testes
- [x] O projeto é organizado em aplicações Django para contas e profissionais, com modelos, views, URLs, migrações, templates HTML, arquivos CSS/JavaScript, formulários validados, administração e comando de carga de categorias.
- [x] Usa Python 3.12, Django 5.2, SQLite, HTML5, CSS3 e JavaScript, com configuração ambiente e instruções para execução local.
- [x] A suíte automatizada contém testes unitários e de integração de cadastro de profissionais, busca por categoria/região, autenticação, validação dos formulários, autorização de edição, WhatsApp, categorias e rotas principais.
- [x] Coverage.py está configurado e foi executado: 24 testes aprovados; relatório textual, XML e HTML derivados da execução efetiva; cobertura total reportada de 94%.

## GitHub e entrega
- [x] A branch local de trabalho `desenvolvimento` foi criada a partir da branch homônima do repositório público. A branch `main` não foi modificada. Foi registrado um commit de implementação com mensagem específica; as evidências e o estado final também foram organizados em commit separado.
- [ ] Enviar `desenvolvimento` ao GitHub e abrir o Pull Request direcionado a `main`: não foi possível nesta execução porque `gh auth status` confirmou que não há sessão GitHub autenticada. O repositório foi acessado somente para leitura; `docs/PULL_REQUEST.md` contém as instruções para concluir o push/PR após autenticação.
- [x] Arquivos preexistentes foram preservados, sem substituições desnecessárias.
- [x] O `README.md` existente não foi criado, removido, substituído nem alterado; seu SHA-256 permaneceu `29fcd4dcc935706b65285149c295cbe18cdfbf039253dd4faf2837e0cee5506d`.
- [x] O ZIP de entrega contém os arquivos necessários, documentação e relatórios verdadeiros, excluindo `.git`, ambiente virtual, banco SQLite local e caches/temporários.
- [x] O servidor Django foi iniciado e as páginas, os recursos estáticos e o manifesto JSON responderam HTTP 200; o projeto está pronto para execução local conforme as instruções de instalação.