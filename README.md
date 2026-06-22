# HealthNews

Sistema para monitorar notícias públicas sobre saúde, RCP, primeiros socorros, simulação realística e áreas relacionadas.

## Funcionalidades

- Login de usuários
- Cadastro de contas com nome personalizado
- Dashboard funcional
- Página de notícias
- Página de sugestões de posts
- Página de aprovações
- Página de configurações
- Busca de notícias públicas via Google News RSS
- Palavras-chave personalizáveis
- Banco local SQLite
- Sugestão simples de legenda para LinkedIn
- Status: pendente, aprovada, publicada e descartada
- Registro do usuário que buscou/adicionou as notícias

## Tecnologias

- Python
- FastAPI
- SQLite
- Feedparser
- HTML/CSS

## Como rodar

Crie e ative o ambiente virtual:

```bash
python -m venv venv
```

No Windows:

```bash
venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute:

```bash
python -m uvicorn app.main:app --reload
```

Abra no navegador:

```text
http://127.0.0.1:8000
```
