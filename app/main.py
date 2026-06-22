from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import init_db
from app.auth_service import create_user, authenticate_user, create_session_token, get_current_user
from app.news_service import (
    fetch_news,
    get_news,
    get_news_by_id,
    update_status,
    delete_news,
    update_post_suggestion,
    get_dashboard_stats,
)
from app.settings_service import get_app_settings, update_app_settings

app = FastAPI(title="HealthNews")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.on_event("startup")
def startup():
    init_db()


def render(request: Request, template: str, context: dict):
    user = get_current_user(request)
    settings = get_app_settings()

    if not user:
        return RedirectResponse("/login", status_code=303)

    context.update({"request": request, "user": user, "settings": settings})
    return templates.TemplateResponse(template, context)


@app.get("/")
def home():
    return RedirectResponse("/dashboard", status_code=303)


@app.get("/login")
def login_page(request: Request):
    if get_current_user(request):
        return RedirectResponse("/dashboard", status_code=303)

    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = authenticate_user(username, password)

    if not user:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Usuário ou senha inválidos."}
        )

    response = RedirectResponse("/dashboard", status_code=303)
    response.set_cookie(
        key="healthnews_session",
        value=create_session_token(user["id"]),
        httponly=True,
        samesite="lax",
    )
    return response


@app.get("/register")
def register_page(request: Request):
    if get_current_user(request):
        return RedirectResponse("/dashboard", status_code=303)

    return templates.TemplateResponse("register.html", {"request": request, "error": None})


@app.post("/register")
def register(
    request: Request,
    display_name: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
):
    if len(username.strip()) < 3:
        return templates.TemplateResponse("register.html", {"request": request, "error": "O usuário precisa ter pelo menos 3 caracteres."})

    if len(password) < 6:
        return templates.TemplateResponse("register.html", {"request": request, "error": "A senha precisa ter pelo menos 6 caracteres."})

    if password != confirm_password:
        return templates.TemplateResponse("register.html", {"request": request, "error": "As senhas não conferem."})

    user_id = create_user(display_name, username, password)

    if not user_id:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Esse nome de usuário já existe."})

    response = RedirectResponse("/dashboard", status_code=303)
    response.set_cookie(
        key="healthnews_session",
        value=create_session_token(user_id),
        httponly=True,
        samesite="lax",
    )
    return response


@app.get("/logout")
def logout():
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie("healthnews_session")
    return response


@app.get("/dashboard")
def dashboard(request: Request):
    stats = get_dashboard_stats()
    return render(request, "dashboard.html", {"active_page": "dashboard", "stats": stats})


@app.post("/fetch-news")
def fetch_news_route(request: Request):
    user = get_current_user(request)

    if not user:
        return RedirectResponse("/login", status_code=303)

    fetch_news(user_id=user["id"])
    return RedirectResponse("/noticias", status_code=303)


@app.get("/noticias")
def noticias(request: Request, busca: str = Query(default="")):
    news = get_news(search=busca if busca else None)
    return render(
        request,
        "noticias.html",
        {"active_page": "noticias", "news": news, "busca": busca, "title": "Todas as notícias"}
    )


@app.get("/sugestoes")
def sugestoes(request: Request):
    news = get_news(status="pendente")
    return render(
        request,
        "sugestoes.html",
        {"active_page": "sugestoes", "news": news, "title": "Sugestões pendentes"}
    )


@app.get("/aprovacoes")
def aprovacoes(request: Request, status: str = Query(default="aprovada")):
    allowed = ["aprovada", "publicada", "descartada"]
    selected_status = status if status in allowed else "aprovada"
    news = get_news(status=selected_status)

    return render(
        request,
        "aprovacoes.html",
        {
            "active_page": "aprovacoes",
            "news": news,
            "selected_status": selected_status,
            "title": "Aprovações",
        }
    )


@app.get("/noticias/{news_id}")
def news_detail(request: Request, news_id: int):
    selected_news = get_news_by_id(news_id)

    if not selected_news:
        return RedirectResponse("/noticias", status_code=303)

    return render(
        request,
        "news_detail.html",
        {"active_page": "noticias", "selected_news": selected_news}
    )


@app.post("/noticias/{news_id}/status")
def change_status(request: Request, news_id: int, status: str = Form(...), redirect_to: str = Form(default="")):
    if not get_current_user(request):
        return RedirectResponse("/login", status_code=303)

    update_status(news_id, status)
    return RedirectResponse(redirect_to or f"/noticias/{news_id}", status_code=303)


@app.post("/noticias/{news_id}/legenda")
def edit_caption(request: Request, news_id: int, post_suggestion: str = Form(...)):
    if not get_current_user(request):
        return RedirectResponse("/login", status_code=303)

    update_post_suggestion(news_id, post_suggestion)
    return RedirectResponse(f"/noticias/{news_id}", status_code=303)


@app.post("/noticias/{news_id}/delete")
def delete_news_route(request: Request, news_id: int):
    if not get_current_user(request):
        return RedirectResponse("/login", status_code=303)

    delete_news(news_id)
    return RedirectResponse("/noticias", status_code=303)


@app.get("/configuracoes")
def configuracoes(request: Request, saved: str = Query(default="")):
    return render(
        request,
        "configuracoes.html",
        {"active_page": "configuracoes", "saved": saved == "1"}
    )


@app.post("/configuracoes")
def salvar_configuracoes(
    request: Request,
    company_name: str = Form(...),
    company_description: str = Form(...),
    keywords: str = Form(...),
):
    if not get_current_user(request):
        return RedirectResponse("/login", status_code=303)

    update_app_settings(company_name, company_description, keywords)
    return RedirectResponse("/configuracoes?saved=1", status_code=303)
