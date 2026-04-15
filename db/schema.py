"""Database schema definition and initialization."""
import os
import sqlite3

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS products (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL UNIQUE,
    vendor      TEXT NOT NULL,
    description TEXT,
    logo_path   TEXT,
    website_url TEXT,
    is_default  INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS industries (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL UNIQUE,
    description TEXT,
    icon_name   TEXT NOT NULL,
    sort_order  INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS features (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    category    TEXT NOT NULL,
    description TEXT,
    data_type   TEXT NOT NULL DEFAULT 'text',
    UNIQUE(name, category)
);

CREATE TABLE IF NOT EXISTS industry_features (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    industry_id INTEGER NOT NULL REFERENCES industries(id) ON DELETE CASCADE,
    feature_id  INTEGER NOT NULL REFERENCES features(id) ON DELETE CASCADE,
    weight      REAL NOT NULL DEFAULT 1.0,
    sort_order  INTEGER NOT NULL DEFAULT 0,
    UNIQUE(industry_id, feature_id)
);

CREATE TABLE IF NOT EXISTS product_features (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id  INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    feature_id  INTEGER NOT NULL REFERENCES features(id) ON DELETE CASCADE,
    value       TEXT NOT NULL,
    source      TEXT,
    updated_at  TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(product_id, feature_id)
);

CREATE TABLE IF NOT EXISTS expert_advice (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    industry_id  INTEGER NOT NULL REFERENCES industries(id) ON DELETE CASCADE,
    product_a_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    product_b_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    advice_text  TEXT NOT NULL,
    author       TEXT,
    created_at   TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS comparison_history (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    product_a_id INTEGER NOT NULL REFERENCES products(id),
    product_b_id INTEGER NOT NULL REFERENCES products(id),
    industry_id  INTEGER NOT NULL REFERENCES industries(id),
    feature_ids  TEXT NOT NULL,
    ppt_path     TEXT,
    llm_summary  TEXT,
    created_at   TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS case_studies (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    industry_id  INTEGER NOT NULL REFERENCES industries(id) ON DELETE CASCADE,
    product_id   INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    title        TEXT NOT NULL,
    customer     TEXT NOT NULL,
    summary      TEXT NOT NULL,
    results      TEXT,
    source_url   TEXT,
    created_at   TEXT NOT NULL DEFAULT (datetime('now'))
);
"""

# TiDB Cloud / MySQL-compatible schema
TIDB_SCHEMA_SQL = [
    """CREATE TABLE IF NOT EXISTS products (
        id          INT PRIMARY KEY AUTO_INCREMENT,
        name        VARCHAR(255) NOT NULL UNIQUE,
        vendor      VARCHAR(255) NOT NULL,
        description TEXT,
        logo_path   TEXT,
        website_url TEXT,
        is_default  INT NOT NULL DEFAULT 0,
        created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    )""",
    """CREATE TABLE IF NOT EXISTS industries (
        id          INT PRIMARY KEY AUTO_INCREMENT,
        name        VARCHAR(255) NOT NULL UNIQUE,
        description TEXT,
        icon_name   VARCHAR(100) NOT NULL,
        sort_order  INT NOT NULL DEFAULT 0
    )""",
    """CREATE TABLE IF NOT EXISTS features (
        id          INT PRIMARY KEY AUTO_INCREMENT,
        name        VARCHAR(255) NOT NULL,
        category    VARCHAR(255) NOT NULL,
        description TEXT,
        data_type   VARCHAR(50) NOT NULL DEFAULT 'text',
        UNIQUE(name, category)
    )""",
    """CREATE TABLE IF NOT EXISTS industry_features (
        id          INT PRIMARY KEY AUTO_INCREMENT,
        industry_id INT NOT NULL,
        feature_id  INT NOT NULL,
        weight      DOUBLE NOT NULL DEFAULT 1.0,
        sort_order  INT NOT NULL DEFAULT 0,
        UNIQUE(industry_id, feature_id)
    )""",
    """CREATE TABLE IF NOT EXISTS product_features (
        id          INT PRIMARY KEY AUTO_INCREMENT,
        product_id  INT NOT NULL,
        feature_id  INT NOT NULL,
        value       TEXT NOT NULL,
        source      TEXT,
        updated_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        UNIQUE(product_id, feature_id)
    )""",
    """CREATE TABLE IF NOT EXISTS expert_advice (
        id           INT PRIMARY KEY AUTO_INCREMENT,
        industry_id  INT NOT NULL,
        product_a_id INT NOT NULL,
        product_b_id INT NOT NULL,
        advice_text  TEXT NOT NULL,
        author       VARCHAR(255),
        created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    )""",
    """CREATE TABLE IF NOT EXISTS comparison_history (
        id           INT PRIMARY KEY AUTO_INCREMENT,
        product_a_id INT NOT NULL,
        product_b_id INT NOT NULL,
        industry_id  INT NOT NULL,
        feature_ids  TEXT NOT NULL,
        ppt_path     TEXT,
        llm_summary  TEXT,
        created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    )""",
    """CREATE TABLE IF NOT EXISTS case_studies (
        id           INT PRIMARY KEY AUTO_INCREMENT,
        industry_id  INT NOT NULL,
        product_id   INT NOT NULL,
        title        VARCHAR(500) NOT NULL,
        customer     VARCHAR(255) NOT NULL,
        summary      TEXT NOT NULL,
        results      TEXT,
        source_url   TEXT,
        created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    )""",
]


def initialize_database(db_path: str = "battlecard.db") -> None:
    """Create all tables and seed data if the database is new."""
    is_new = not os.path.exists(db_path)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA_SQL)
    conn.commit()

    if is_new:
        _seed_data(conn)

    conn.close()


def _seed_data(conn: sqlite3.Connection) -> None:
    """Load seed data from seed_data.sql if it exists."""
    seed_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "seed_data.sql")
    if os.path.exists(seed_path):
        with open(seed_path, "r", encoding="utf-8") as f:
            conn.executescript(f.read())


def initialize_tidb_database(conn) -> None:
    """Create all tables and seed data on TiDB Cloud Serverless."""
    cursor = conn.cursor()
    for stmt in TIDB_SCHEMA_SQL:
        cursor.execute(stmt)
    conn.commit()

    # Seed if products table is empty
    cursor.execute("SELECT COUNT(*) AS cnt FROM products")
    if cursor.fetchone()["cnt"] == 0:
        _seed_tidb_data(conn)


def _seed_tidb_data(conn) -> None:
    """Load seed data into TiDB (execute statements one by one)."""
    seed_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "seed_data.sql")
    if not os.path.exists(seed_path):
        return
    with open(seed_path, "r", encoding="utf-8") as f:
        sql = f.read()
    cursor = conn.cursor()
    for stmt in sql.split(";"):
        stmt = stmt.strip()
        if stmt and not stmt.startswith("--"):
            cursor.execute(stmt)
    conn.commit()
