"""
Nightly loans report, uploaded to the school's cloud storage bucket.
"""

import datetime
import json
import os
import urllib.request

import db
import loans

BUCKET_URL = "https://files.cloudvault.example/binarybay-library/reports/"


def load_credentials():
    """Read the storage credentials from the .env file next to this script."""
    values = {}
    env_path = os.path.join(os.path.dirname(__file__), ".env")

    if not os.path.exists(env_path):
        return values

    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip()

    return values


def build_report():
    conn = db.connect()
    open_loans = conn.execute(
        "SELECT COUNT(*) FROM loans WHERE returned_on IS NULL"
    ).fetchone()[0]
    titles = conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    conn.close()

    overdue = loans.overdue_loans()

    return {
        "generated": datetime.datetime.now().strftime("%Y-%m-%d"),
        "titles_held": titles,
        "loans_open": open_loans,
        "loans_overdue": len(overdue),
        "fines_outstanding": round(sum(loans.fine_for(l) for l in overdue), 2),
    }


def upload_nightly(demo=False):
    report = build_report()
    filename = "loans-%s.json" % datetime.datetime.now().strftime("%Y-%m-%d")

    if demo:
        print("[demo] would upload %s to %s" % (filename, BUCKET_URL))
        for key, value in report.items():
            print("[demo]   %-18s %s" % (key, value))
        return

    credentials = load_credentials()
    key = credentials.get("CLOUDVAULT_ACCESS_KEY", "")
    secret = credentials.get("CLOUDVAULT_SECRET_KEY", "")

    if not key or not secret:
        print("Storage credentials are missing. Cannot upload.")
        return

    payload = json.dumps(report).encode()
    request = urllib.request.Request(BUCKET_URL + filename, data=payload,
                                     method="PUT")
    request.add_header("X-Access-Key", key)
    request.add_header("X-Secret-Key", secret)

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            print("Uploaded %s (%d)" % (filename, response.status))
    except Exception as error:
        print("Could not upload report: %s" % error)


def _redact(db_url):
    """Hide the password when printing a connection string."""
    if "://" not in db_url or "@" not in db_url:
        return db_url
    scheme, rest = db_url.split("://", 1)
    credentials, host = rest.split("@", 1)
    user = credentials.split(":", 1)[0]
    return "%s://%s:****@%s" % (scheme, user, host)


def rows_to_sync():
    """Loans that have changed since the last office sync."""
    conn = db.connect()
    rows = conn.execute(
        "SELECT id, book_id, student_id, borrowed_on, due_on, returned_on "
        "FROM loans ORDER BY id"
    ).fetchall()
    conn.close()
    return rows


def sync_to_office(db_url, demo=False):
    """Push loan records up to the office database."""
    rows = rows_to_sync()

    if demo:
        print("[demo] would sync %d loan records" % len(rows))
        print("[demo] target: %s" % _redact(db_url))
        return

    try:
        import psycopg2
    except ImportError:
        print("psycopg2 is not installed on this machine, so the office sync "
              "cannot run here. It runs on the library terminal overnight.")
        return

    try:
        conn = psycopg2.connect(db_url)
    except Exception as error:
        print("Could not reach the office database: %s" % error)
        return

    cursor = conn.cursor()
    for row in rows:
        cursor.execute(
            "INSERT INTO loans (id, book_id, student_id, borrowed_on, "
            "due_on, returned_on) VALUES (%s, %s, %s, %s, %s, %s) "
            "ON CONFLICT (id) DO UPDATE SET returned_on = EXCLUDED.returned_on",
            tuple(row),
        )
    conn.commit()
    conn.close()
    print("Synced %d loan records to the office." % len(rows))
