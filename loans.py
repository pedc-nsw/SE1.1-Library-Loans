"""
Checking books out, returning them, and tracking what is overdue.
"""

import datetime

import config
import db


def _today():
    return datetime.date.today()


def checkout(book_id, student_id):
    conn = db.connect()

    book = conn.execute("SELECT * FROM books WHERE id = ?",
                        (book_id,)).fetchone()
    student = conn.execute("SELECT * FROM students WHERE id = ?",
                           (student_id,)).fetchone()

    if book is None:
        print("No book with id %d" % book_id)
        conn.close()
        return
    if student is None:
        print("No student with id %d" % student_id)
        conn.close()
        return

    available = book["copies"] - book["on_loan"]
    if available < 1:
        print("All %d copies of '%s' are already on loan."
              % (book["copies"], book["title"]))
        conn.close()
        return

    borrowed = _today()
    due = borrowed + datetime.timedelta(days=config.LOAN_PERIOD_DAYS)

    conn.execute(
        "INSERT INTO loans (book_id, student_id, borrowed_on, due_on, "
        "returned_on) VALUES (?, ?, ?, ?, NULL)",
        (book_id, student_id, borrowed.isoformat(), due.isoformat()),
    )
    conn.execute("UPDATE books SET on_loan = on_loan + 1 WHERE id = ?",
                 (book_id,))
    conn.commit()
    conn.close()

    print("'%s' checked out to %s. Due %s."
          % (book["title"], student["name"], due.isoformat()))


def return_book(book_id):
    conn = db.connect()

    loan = conn.execute(
        "SELECT loans.*, books.title, students.name FROM loans "
        "JOIN books ON books.id = loans.book_id "
        "JOIN students ON students.id = loans.student_id "
        "WHERE loans.book_id = ? AND loans.returned_on IS NULL "
        "ORDER BY loans.due_on LIMIT 1",
        (book_id,),
    ).fetchone()

    if loan is None:
        print("No open loan for book %d" % book_id)
        conn.close()
        return

    conn.execute("UPDATE loans SET returned_on = ? WHERE id = ?",
                 (_today().isoformat(), loan["id"]))
    conn.execute("UPDATE books SET on_loan = on_loan - 1 WHERE id = ?",
                 (book_id,))
    conn.commit()
    conn.close()

    days_late = (_today() - datetime.date.fromisoformat(loan["due_on"])).days
    print("'%s' returned by %s." % (loan["title"], loan["name"]))
    if days_late > 0:
        print("%d days late. Fine: $%.2f"
              % (days_late, days_late * config.FINE_PER_DAY))


def overdue_loans():
    """Return every loan that is past its due date and not yet returned."""
    conn = db.connect()
    rows = conn.execute(
        "SELECT loans.*, books.title, students.name, students.email "
        "FROM loans "
        "JOIN books ON books.id = loans.book_id "
        "JOIN students ON students.id = loans.student_id "
        "WHERE loans.returned_on IS NULL AND loans.due_on < ? "
        "ORDER BY loans.due_on",
        (_today().isoformat(),),
    ).fetchall()
    conn.close()
    return rows


def days_overdue(loan):
    return (_today() - datetime.date.fromisoformat(loan["due_on"])).days


def fine_for(loan):
    return days_overdue(loan) * config.FINE_PER_DAY


def print_overdue():
    rows = overdue_loans()

    if not rows:
        print("Nothing is overdue.")
        return

    print("%-26s %-18s %6s %8s" % ("TITLE", "STUDENT", "DAYS", "FINE"))
    print("-" * 62)
    for row in rows:
        print("%-26s %-18s %6d %8.2f" % (
            row["title"][:26], row["name"][:18],
            days_overdue(row), fine_for(row)))
