# 💙 HealthNews

Sistema web desenvolvido em **Python** para monitorar notícias públicas relacionadas à saúde, RCP, primeiros socorros, simulação realística e áreas relacionadas.  
O projeto foi pensado para auxiliar empresas da área da saúde na curadoria de conteúdos relevantes e na criação de sugestões de posts para o LinkedIn.

---

# 🇧🇷 **VERSÃO EM PORTUGUÊS**

## 📌 Sobre o projeto

O **HealthNews** é uma aplicação web criada para buscar notícias públicas na internet sobre temas ligados à área da saúde, como **RCP**, **reanimação cardiopulmonar**, **primeiros socorros**, **emergências médicas**, **simuladores médicos** e **simulação realística**.

A ideia principal do projeto é ajudar empresas que trabalham com produtos de RCP, treinamentos e simuladores a encontrarem conteúdos relevantes para publicar no LinkedIn de forma mais organizada, rápida e profissional.

O sistema busca notícias, salva os dados em um banco local, gera uma sugestão simples de legenda e permite que os usuários revisem, aprovem, publiquem ou descartem os conteúdos.

---

## 🚀 Funcionalidades

- Cadastro de usuários
- Login com sessão protegida
- Nome personalizado para cada usuário
- Dashboard com resumo geral
- Busca de notícias públicas via Google News RSS
- Filtro por palavras-chave
- Página de notícias
- Página de sugestões de posts
- Página de aprovações
- Página de configurações
- Edição das palavras-chave de busca
- Edição do nome e descrição do sistema
- Geração de legenda sugerida para LinkedIn
- Edição manual da legenda sugerida
- Status para cada notícia:
  - Pendente
  - Aprovada
  - Publicada
  - Descartada
- Registro do usuário que adicionou/buscou as notícias
- Banco de dados local com SQLite
- Interface web simples, organizada e responsiva

---

## 🛠️ Tecnologias utilizadas

- Python
- FastAPI
- Uvicorn
- SQLite
- Feedparser
- Jinja2
- HTML
- CSS
- Google News RSS

---

## 📂 Estrutura do projeto

```bash
healthnews/
├── app/
│   ├── static/
│   │   └── style.css
│   ├── templates/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── noticias.html
│   │   ├── sugestoes.html
│   │   ├── aprovacoes.html
│   │   ├── configuracoes.html
│   │   ├── news_detail.html
│   │   ├── login.html
│   │   └── register.html
│   ├── __init__.py
│   ├── auth_service.py
│   ├── database.py
│   ├── main.py
│   ├── news_service.py
│   └── settings_service.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Como executar o projeto

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
```

Entre na pasta do projeto:

```bash
cd seu-repositorio
```

Crie o ambiente virtual:

```bash
python -m venv venv
```

Ative o ambiente virtual no Windows:

```bash
venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o servidor:

```bash
python -m uvicorn app.main:app --reload
```

Abra no navegador:

```text
http://127.0.0.1:8000
```

---

## 👤 Como usar

Ao abrir o sistema pela primeira vez, será exibida a tela de login.

Caso ainda não tenha uma conta, clique em **Criar conta** e cadastre:

- Nome de exibição
- Nome de usuário
- Senha

Depois de entrar, o usuário terá acesso ao painel principal do sistema.

---

## 🧭 Páginas do sistema

### 🏠 Dashboard

Mostra um resumo geral das notícias encontradas, conteúdos pendentes, aprovados e publicados.

### 📰 Notícias

Lista todas as notícias encontradas pelo sistema.  
Também permite pesquisar, abrir a notícia original, visualizar detalhes e alterar seu status.

### ✍️ Sugestões

Mostra as notícias pendentes com legendas sugeridas para revisão.

### ✅ Aprovações

Organiza os conteúdos por status:

- Aprovadas
- Publicadas
- Descartadas

### ⚙️ Configurações

Permite editar:

- Nome do sistema
- Descrição curta
- Palavras-chave usadas para buscar notícias

---

## 🔎 Como funciona a busca de notícias

O sistema utiliza o **Google News RSS** para buscar notícias públicas com base nas palavras-chave cadastradas.

Exemplos de palavras-chave:

```text
RCP
reanimação cardiopulmonar
primeiros socorros
parada cardíaca
emergência médica
simulação realística
simuladores médicos
treinamento em saúde
APH
SAMU
educação em saúde
```

As notícias encontradas são salvas no banco de dados local e organizadas por categoria.

---

## 📝 Sugestão de legenda para LinkedIn

Para cada notícia encontrada, o sistema gera uma legenda simples que pode ser usada como base para publicação no LinkedIn.

A legenda pode ser editada manualmente antes de ser aprovada ou publicada.

> O sistema não publica automaticamente no LinkedIn. A publicação deve ser feita manualmente após revisão humana.

---

## 🔐 Segurança

O projeto possui:

- Senhas salvas com hash
- Sessão protegida por cookie assinado
- Banco de dados local SQLite

Para uso profissional em produção, seria recomendado adicionar:

- HTTPS
- controle de permissões por cargo
- recuperação de senha
- logs de acesso
- banco de dados em servidor
- autenticação mais robusta

---

## 🎯 Objetivo do projeto

O objetivo do **HealthNews** é facilitar a curadoria de notícias da área da saúde e ajudar empresas a criarem conteúdos relevantes para redes profissionais, principalmente o LinkedIn.

O projeto também demonstra conhecimentos em:

- desenvolvimento web com Python
- criação de APIs com FastAPI
- autenticação de usuários
- banco de dados SQLite
- consumo de RSS
- organização de dados
- criação de interface web
- automação de processos

---

## 📌 Status do projeto

Projeto em desenvolvimento.  
A versão atual possui as principais funcionalidades do MVP funcionando localmente.

---

## 👩‍💻 Desenvolvido por

Projeto desenvolvido por **Andrew R**.

---

<br>

# 🇺🇸 **ENGLISH VERSION**

## 📌 About the Project

**HealthNews** is a web application created to search for public news related to healthcare topics such as **CPR**, **cardiopulmonary resuscitation**, **first aid**, **medical emergencies**, **medical simulators**, and **realistic simulation**.

The main goal of this project is to help companies that work with CPR products, training solutions, and healthcare simulators find relevant content to publish on LinkedIn in a more organized, fast, and professional way.

The system searches for news, stores the data in a local database, generates a simple LinkedIn caption suggestion, and allows users to review, approve, publish, or discard the content.

---

## 🚀 Features

- User registration
- Login with protected session
- Custom display name for each user
- Dashboard with general overview
- Public news search using Google News RSS
- Keyword-based filtering
- News page
- Post suggestions page
- Approval page
- Settings page
- Editable search keywords
- Editable system name and description
- LinkedIn caption suggestion generation
- Manual editing of suggested captions
- Status for each news item:
  - Pending
  - Approved
  - Published
  - Discarded
- Tracks which user added/searched the news
- Local SQLite database
- Simple, organized, and responsive web interface

---

## 🛠️ Technologies Used

- Python
- FastAPI
- Uvicorn
- SQLite
- Feedparser
- Jinja2
- HTML
- CSS
- Google News RSS

---

## 📂 Project Structure

```bash
healthnews/
├── app/
│   ├── static/
│   │   └── style.css
│   ├── templates/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── noticias.html
│   │   ├── sugestoes.html
│   │   ├── aprovacoes.html
│   │   ├── configuracoes.html
│   │   ├── news_detail.html
│   │   ├── login.html
│   │   └── register.html
│   ├── __init__.py
│   ├── auth_service.py
│   ├── database.py
│   ├── main.py
│   ├── news_service.py
│   └── settings_service.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ How to Run the Project

Clone the repository:

```bash
git clone https://github.com/your-username/your-repository.git
```

Enter the project folder:

```bash
cd your-repository
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the server:

```bash
python -m uvicorn app.main:app --reload
```

Open in your browser:

```text
http://127.0.0.1:8000
```

---

## 👤 How to Use

When opening the system for the first time, the login page will be displayed.

If you do not have an account yet, click **Create account** and register:

- Display name
- Username
- Password

After logging in, the user will have access to the main system dashboard.

---

## 🧭 System Pages

### 🏠 Dashboard

Displays a general overview of found news, pending content, approved content, and published content.

### 📰 News

Lists all news found by the system.  
It also allows users to search, open the original news source, view details, and update the news status.

### ✍️ Suggestions

Displays pending news with suggested LinkedIn captions for review.

### ✅ Approvals

Organizes content by status:

- Approved
- Published
- Discarded

### ⚙️ Settings

Allows users to edit:

- System name
- Short description
- Keywords used to search for news

---

## 🔎 How the News Search Works

The system uses **Google News RSS** to search for public news based on registered keywords.

Examples of keywords:

```text
CPR
cardiopulmonary resuscitation
first aid
cardiac arrest
medical emergency
realistic simulation
medical simulators
healthcare training
emergency care
health education
```

The news found is stored in a local database and organized by category.

---

## 📝 LinkedIn Caption Suggestion

For each news item found, the system generates a simple caption that can be used as a base for a LinkedIn post.

The caption can be manually edited before being approved or published.

> The system does not automatically publish to LinkedIn. Publishing must be done manually after human review.

---

## 🔐 Security

The project includes:

- Password hashing
- Session protected by signed cookies
- Local SQLite database

For professional production use, it would be recommended to add:

- HTTPS
- role-based permissions
- password recovery
- access logs
- server-based database
- stronger authentication

---

## 🎯 Project Goal

The goal of **HealthNews** is to make healthcare news curation easier and help companies create relevant content for professional social media, especially LinkedIn.

The project also demonstrates knowledge in:

- web development with Python
- API development with FastAPI
- user authentication
- SQLite database
- RSS consumption
- data organization
- web interface creation
- process automation

---

## 📌 Project Status

Project under development.  
The current version includes the main MVP features running locally.

---

## 👩‍💻 Developed by

Project developed by **Andrew R**.
