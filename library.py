"""
Binary Bay High Library - Loans Management
Command line tool for library staff.

Usage:
    python library.py setup
    python library.py search <term>
    python library.py checkout <book_id> <student_id>
    python library.py return <book_id>
"""

import argparse
import sys

import config
import db
import catalogue
import loans


def build_parser():
    parser = argparse.ArgumentParser(description="Library loans management")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("setup", help="Create the database and load sample data")

    p_search = sub.add_parser("search", help="Search the catalogue")
    p_search.add_argument("term")

    p_out = sub.add_parser("checkout", help="Check a book out to a student")
    p_out.add_argument("book_id", type=int)
    p_out.add_argument("student_id", type=int)

    p_ret = sub.add_parser("return", help="Return a book")
    p_ret.add_argument("book_id", type=int)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 0

    if args.command == "setup":
        db.initialise()
        print("Database ready at %s" % config.LOCAL_DB)

    elif args.command == "search":
        catalogue.search(args.term)

    elif args.command == "checkout":
        loans.checkout(args.book_id, args.student_id)

    elif args.command == "return":
        loans.return_book(args.book_id)

    return 0


if __name__ == "__main__":
    sys.exit(main())
