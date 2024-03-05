"""
Overdue notices, emailed to students.

Sent through the mail provider the school already pays for.
"""

import json
import urllib.request

import config
import loans

MAIL_API_URL = "https://api.mailsend.example/v3/mail/send"
MAIL_API_KEY = "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"


def build_body(loan):
    return (
        "Hi %s,\n\n"
        "The library book below is overdue.\n\n"
        "  %s\n"
        "  Due: %s (%d days ago)\n"
        "  Fine so far: $%.2f\n\n"
        "Please return it to the library desk before school ends on Friday.\n\n"
        "Binary Bay High Library"
    ) % (
        loan["name"],
        loan["title"],
        loan["due_on"],
        loans.days_overdue(loan),
        loans.fine_for(loan),
    )


def send_overdue_notices(demo=False):
    overdue = loans.overdue_loans()

    if not overdue:
        print("Nothing is overdue. No notices to send.")
        return

    for loan in overdue:
        body = build_body(loan)

        if demo:
            print("[demo] would email %s" % loan["email"])
            print("-" * 62)
            print(body)
            print("-" * 62)
            continue

        payload = json.dumps({
            "personalizations": [{"to": [{"email": loan["email"]}]}],
            "from": {"email": config.FROM_ADDRESS},
            "subject": "Overdue library book: %s" % loan["title"],
            "content": [{"type": "text/plain", "value": body}],
        }).encode()

        request = urllib.request.Request(MAIL_API_URL, data=payload)
        request.add_header("Authorization", "Bearer " + MAIL_API_KEY)
        request.add_header("Content-Type", "application/json")

        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                print("Notice sent to %s (%d)"
                      % (loan["email"], response.status))
        except Exception as error:
            print("Could not send notice to %s: %s" % (loan["email"], error))

    print("%d overdue loan(s) processed." % len(overdue))
