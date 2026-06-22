from app.database import get_connection, DEFAULT_KEYWORDS


def get_setting(key: str, default: str = "") -> str:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return default

    return row["value"]


def set_setting(key: str, value: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO settings (key, value)
        VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value
    """, (key, value))
    conn.commit()
    conn.close()


def get_app_settings():
    keywords_text = get_setting("keywords", "\n".join(DEFAULT_KEYWORDS))
    keywords = [line.strip() for line in keywords_text.splitlines() if line.strip()]

    return {
        "company_name": get_setting("company_name", "HealthNews"),
        "company_description": get_setting("company_description", "Conteúdo que salva vidas"),
        "keywords_text": keywords_text,
        "keywords": keywords,
    }


def update_app_settings(company_name: str, company_description: str, keywords_text: str):
    set_setting("company_name", company_name.strip() or "HealthNews")
    set_setting("company_description", company_description.strip() or "Conteúdo que salva vidas")
    set_setting("keywords", keywords_text.strip())
