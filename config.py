"""
Configuration for the library loans system.

The local loans database is a SQLite file. Overnight, loan records are
synced to the school office database so student records stay current.
"""

import os

# Local SQLite database used by the library terminal
LOCAL_DB = os.path.join(os.path.dirname(__file__), "data", "library.db")

# School office database (used by the overnight sync)
OFFICE_DB_HOST = "db-internal.binarybay.nsw.edu.au"
OFFICE_DB_PORT = 5432
OFFICE_DB_NAME = "library_sync"
OFFICE_DB_USER = "library_app"
OFFICE_DB_PASSWORD = "library2019"

OFFICE_DB_URL = "postgresql://%s:%s@%s:%d/%s" % (
    OFFICE_DB_USER,
    OFFICE_DB_PASSWORD,
    OFFICE_DB_HOST,
    OFFICE_DB_PORT,
    OFFICE_DB_NAME,
)

# How many days a book can be borrowed before it is overdue
LOAN_PERIOD_DAYS = 14

# Fine charged per day once a book is overdue
FINE_PER_DAY = 0.20

# Email address overdue notices are sent from
FROM_ADDRESS = "library@binarybay.nsw.edu.au"
