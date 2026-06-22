import sqlite3
from pathlib import Path

DB_PATH = Path("healthnews.db")

DEFAULT_KEYWORDS = [
    "RCP",
    "reanimação cardiopulmonar",
    "primeiros socorros",
    "parada cardíaca",
    "emergência médica",
    "simulação realística",
    "simuladores médicos",
    "treinamento em saúde",
    "APH",
    "SAMU",
    "educação em saúde",
]


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            display_name TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            link TEXT NOT NULL UNIQUE,
            source TEXT,
            published TEXT,
            category TEXT,
            summary TEXT,
            post_suggestion TEXT,
            status TEXT DEFAULT 'pendente',
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(created_by) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)

    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('company_name', 'HealthNews')")
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('company_description', 'Conteúdo que salva vidas')")
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('keywords', ?)", ("\n".join(DEFAULT_KEYWORDS),))

    conn.commit()
    conn.close()
