"""
Password hashing for library staff accounts.

Staff log in at the library terminal to check books in and out.
"""

import hashlib

# Salt applied to every staff password before hashing
PASSWORD_SALT = "EtgOdx2iFdG3G9pzMyswoyZs"

HASH_ITERATIONS = 100000


def hash_password(password):
    """Return the hash of a password as a hex string."""
    derived = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        PASSWORD_SALT.encode(),
        HASH_ITERATIONS,
    )
    return derived.hex()


def verify_password(password, stored_hash):
    """Return True if the password matches the stored hash."""
    return hash_password(password) == stored_hash
