"""
Catalogue search and ISBN lookup.

New books are added by scanning the barcode, then looking the ISBN up
against the schools catalogue service so staff do not have to type the
title and author by hand.
"""

import json
import urllib.request

import db

ISBN_LOOKUP_URL = "https://api.schoolscatalogue.example/v2/books/%s"
CATALOGUE_API_KEY = "oYgV0pViGWUueUb7RR854hbAbI2JFalpopLPhAUlbaVMQirr"


def search(term):
    """Print catalogue entries matching a title or author."""
    conn = db.connect()
    pattern = "%" + term + "%"
    rows = conn.execute(
        "SELECT * FROM books WHERE title LIKE ? OR author LIKE ? "
        "ORDER BY title",
        (pattern, pattern),
    ).fetchall()
    conn.close()

    if not rows:
        print("Nothing in the catalogue matches '%s'." % term)
        return

    print("%-4s %-34s %-22s %8s" % ("ID", "TITLE", "AUTHOR", "AVAIL"))
    print("-" * 72)
    for row in rows:
        available = row["copies"] - row["on_loan"]
        print("%-4d %-34s %-22s %8d" % (
            row["id"], row["title"][:34], row["author"][:22], available))


def lookup_isbn(isbn, demo=False):
    """Fetch the title and author for an ISBN from the catalogue service."""
    if demo:
        print("[demo] would look up ISBN %s" % isbn)
        print("[demo] endpoint: %s" % (ISBN_LOOKUP_URL % isbn))
        return

    request = urllib.request.Request(ISBN_LOOKUP_URL % isbn)
    request.add_header("X-Api-Key", CATALOGUE_API_KEY)

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            record = json.loads(response.read().decode())
            print("%s - %s" % (record.get("title"), record.get("author")))
    except Exception as error:
        print("Could not look up that ISBN: %s" % error)
