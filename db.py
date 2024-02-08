"""
Database setup and connection handling for the local loans database.
"""

import os
import sqlite3

import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS books (
    id        INTEGER PRIMARY KEY,
    isbn      TEXT,
    title     TEXT NOT NULL,
    author    TEXT NOT NULL,
    category  TEXT NOT NULL,
    copies    INTEGER NOT NULL DEFAULT 1,
    on_loan   INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS students (
    id         INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    year_group INTEGER NOT NULL,
    email      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS loans (
    id          INTEGER PRIMARY KEY,
    book_id     INTEGER NOT NULL,
    student_id  INTEGER NOT NULL,
    borrowed_on TEXT NOT NULL,
    due_on      TEXT NOT NULL,
    returned_on TEXT
);

CREATE TABLE IF NOT EXISTS staff (
    id            INTEGER PRIMARY KEY,
    username      TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role          TEXT NOT NULL DEFAULT 'assistant'
);
"""


def connect():
    """Open a connection to the local loans database."""
    folder = os.path.dirname(config.LOCAL_DB)
    if not os.path.exists(folder):
        os.makedirs(folder)

    conn = sqlite3.connect(config.LOCAL_DB)
    conn.row_factory = sqlite3.Row
    return conn


def initialise():
    """Create the tables and load the seed data if the database is empty."""
    conn = connect()
    conn.executescript(SCHEMA)

    count = conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    if count == 0:
        _load_seed_data(conn)

    conn.commit()
    conn.close()


def _load_seed_data(conn):
    import datetime
    import json

    seed_path = os.path.join(os.path.dirname(__file__), "data", "seed.json")
    if not os.path.exists(seed_path):
        return

    with open(seed_path) as f:
        seed = json.load(f)

    # Loan dates in the seed file are stored as "days ago" so that the
    # sample data still looks sensible whenever it is loaded.
    today = datetime.date.today()
    for loan in seed["loans"]:
        borrowed = today - datetime.timedelta(days=loan["borrowed_days_ago"])
        due = borrowed + datetime.timedelta(days=config.LOAN_PERIOD_DAYS)
        loan["borrowed_on"] = borrowed.isoformat()
        loan["due_on"] = due.isoformat()
        loan["returned_on"] = due.isoformat() if loan["returned"] else None

    conn.executemany(
        "INSERT INTO books (id, isbn, title, author, category, copies, on_loan) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        [
            (b["id"], b["isbn"], b["title"], b["author"], b["category"],
             b["copies"], b["on_loan"])
            for b in seed["books"]
        ],
    )
    conn.executemany(
        "INSERT INTO students (id, name, year_group, email) VALUES (?, ?, ?, ?)",
        [(s["id"], s["name"], s["year_group"], s["email"])
         for s in seed["students"]],
    )
    conn.executemany(
        "INSERT INTO loans (id, book_id, student_id, borrowed_on, due_on, "
        "returned_on) VALUES (?, ?, ?, ?, ?, ?)",
        [
            (l["id"], l["book_id"], l["student_id"], l["borrowed_on"],
             l["due_on"], l["returned_on"])
            for l in seed["loans"]
        ],
    )
