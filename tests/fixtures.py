"""
Shared test data.

The payment values below are the sample values from the payment provider's
public documentation. They are not connected to any real account and are
only here so the fines tests have something to run against. Online fine
payment is not finished yet - see the notes in the project board.
"""

# Sample test values from the provider documentation
SAMPLE_PUBLISHABLE_KEY = "pk_test_TYooMQauvdEDq54NiTphI7jx"
SAMPLE_SECRET_KEY = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"
SAMPLE_CARD_NUMBER = "4242424242424242"

SAMPLE_BOOKS = [
    {"id": 3, "title": "Macbeth", "author": "William Shakespeare",
     "copies": 30, "on_loan": 11},
    {"id": 9, "title": "Maths in Focus Year 12", "author": "Grove",
     "copies": 40, "on_loan": 22},
    {"id": 12, "title": "Introduction to Algorithms", "author": "Cormen et al",
     "copies": 4, "on_loan": 4},
]

SAMPLE_OVERDUE = [
    {"id": 5001, "title": "Macbeth", "name": "Liam O'Connell",
     "due_on": "2024-05-01", "days": 17},
    {"id": 5002, "title": "Maths in Focus Year 12", "name": "Jack Petrakis",
     "due_on": "2024-05-06", "days": 12},
]
