import feedparser
from urllib.parse import quote_plus

from app.database import get_connection
from app.settings_service import get_app_settings

CATEGORIES = {
    "RCP": ["RCP", "reanimação cardiopulmonar", "parada cardíaca"],
    "Primeiros Socorros": ["primeiros socorros"],
    "Simulação Realística": ["simulação realística", "simuladores médicos", "simuladores"],
    "Emergência": ["emergência médica", "APH", "SAMU"],
    "Educação em Saúde": ["treinamento em saúde", "educação em saúde", "faculdade", "capacitação"],
}


def detect_category(text: str) -> str:
    text_lower = text.lower()

    for category, terms in CATEGORIES.items():
        for term in terms:
            if term.lower() in text_lower:
                return category

    return "Saúde"


def generate_post_suggestion(title: str, link: str, category: str, company_name: str) -> str:
    hashtags = {
        "RCP": "#RCP #PrimeirosSocorros #Saúde #Treinamento",
        "Primeiros Socorros": "#PrimeirosSocorros #Saúde #Prevenção #Treinamento",
        "Simulação Realística": "#SimulaçãoRealística #EducaçãoEmSaúde #Treinamento #Saúde",
        "Emergência": "#Emergência #APH #SAMU #Saúde #Treinamento",
        "Educação em Saúde": "#EducaçãoEmSaúde #Capacitação #Saúde #Treinamento",
        "Saúde": "#Saúde #Treinamento #EducaçãoEmSaúde",
    }

    return f"""Notícias recentes reforçam a importância de temas como {category}.

📌 {title}

A capacitação e o treinamento contínuo são essenciais para preparar profissionais, instituições e equipes para situações reais.

Na {company_name}, acreditamos que informação, prática e treinamento de qualidade ajudam a construir ambientes mais preparados e seguros.

Leia mais na fonte original:
{link}

{hashtags.get(category, "#Saúde #Treinamento")}"""


def fetch_news(user_id=None):
    app_settings = get_app_settings()
    keywords = app_settings["keywords"]

    if not keywords:
        return 0

    query = " OR ".join(keywords)
    encoded_query = quote_plus(query)

    rss_url = (
        f"https://news.google.com/rss/search?q={encoded_query}"
        "&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    )

    feed = feedparser.parse(rss_url)
    saved_count = 0

    conn = get_connection()
    cursor = conn.cursor()

    for entry in feed.entries:
        title = entry.get("title", "").strip()
        link = entry.get("link", "").strip()
        published = entry.get("published", "")
        source = "Google News"
        summary = entry.get("summary", "")

        if not title or not link:
            continue

        searchable_text = f"{title} {summary}"
        category = detect_category(searchable_text)
        post_suggestion = generate_post_suggestion(
            title=title,
            link=link,
            category=category,
            company_name=app_settings["company_name"],
        )

        try:
            cursor.execute("""
                INSERT INTO news (
                    title, link, source, published, category, summary,
                    post_suggestion, created_by
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (title, link, source, published, category, summary, post_suggestion, user_id))
            saved_count += 1
        except Exception:
            pass

    conn.commit()
    conn.close()
    return saved_count


def get_news(status: str | None = None, search: str | None = None):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT news.*, users.display_name AS creator_name
        FROM news
        LEFT JOIN users ON users.id = news.created_by
        WHERE 1 = 1
    """
    params = []

    if status:
        query += " AND news.status = ?"
        params.append(status)

    if search:
        query += " AND (news.title LIKE ? OR news.category LIKE ? OR news.summary LIKE ?)"
        like_search = f"%{search}%"
        params.extend([like_search, like_search, like_search])

    query += " ORDER BY news.created_at DESC"

    cursor.execute(query, params)
    news = cursor.fetchall()
    conn.close()
    return news


def get_news_by_id(news_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT news.*, users.display_name AS creator_name
        FROM news
        LEFT JOIN users ON users.id = news.created_by
        WHERE news.id = ?
    """, (news_id,))
    news = cursor.fetchone()
    conn.close()
    return news


def update_status(news_id: int, status: str):
    allowed_status = ["pendente", "aprovada", "publicada", "descartada"]

    if status not in allowed_status:
        return False

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE news SET status = ? WHERE id = ?", (status, news_id))
    conn.commit()
    conn.close()
    return True


def delete_news(news_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM news WHERE id = ?", (news_id,))
    conn.commit()
    conn.close()


def update_post_suggestion(news_id: int, post_suggestion: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE news SET post_suggestion = ? WHERE id = ?", (post_suggestion, news_id))
    conn.commit()
    conn.close()


def get_dashboard_stats():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM news")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM news WHERE status = 'pendente'")
    pending = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM news WHERE status = 'aprovada'")
    approved = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM news WHERE status = 'publicada'")
    published = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM news WHERE status = 'descartada'")
    discarded = cursor.fetchone()[0]

    cursor.execute("""
        SELECT category, COUNT(*) as total
        FROM news
        GROUP BY category
        ORDER BY total DESC
    """)
    categories = cursor.fetchall()

    cursor.execute("""
        SELECT users.display_name, COUNT(news.id) AS total
        FROM users
        LEFT JOIN news ON users.id = news.created_by
        GROUP BY users.id
        ORDER BY total DESC
    """)
    users = cursor.fetchall()

    cursor.execute("""
        SELECT news.*, users.display_name AS creator_name
        FROM news
        LEFT JOIN users ON users.id = news.created_by
        ORDER BY news.created_at DESC
        LIMIT 5
    """)
    recent_news = cursor.fetchall()

    conn.close()

    return {
        "total": total,
        "pending": pending,
        "approved": approved,
        "published": published,
        "discarded": discarded,
        "categories": categories,
        "users": users,
        "recent_news": recent_news,
    }
