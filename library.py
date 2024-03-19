"""
Binary Bay High Library - Loans Management
Command line tool for library staff.

Usage:
    python library.py setup
    python library.py search <term>
    python library.py checkout <book_id> <student_id>
    python library.py return <book_id>
    python library.py overdue
    python library.py notify
    python library.py lookup <isbn>

Add --demo to any command to run without contacting external services.
"""

import argparse
import sys

import config
import db
import catalogue
import loans
import notices

def build_parser():
    # --demo is accepted before or after the command name
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--demo", action="store_true",
                        help="Run without contacting external services")

    parser = argparse.ArgumentParser(description="Library loans management",
                                     parents=[common])

    sub = parser.add_subparsers(dest="command")

    sub.add_parser("setup", help="Create the database and load sample data",
                   parents=[common])

    p_search = sub.add_parser("search", help="Search the catalogue",
                              parents=[common])
    p_search.add_argument("term")

    p_out = sub.add_parser("checkout", help="Check a book out to a student",
                           parents=[common])
    p_out.add_argument("book_id", type=int)
    p_out.add_argument("student_id", type=int)

    p_ret = sub.add_parser("return", help="Return a book", parents=[common])
    p_ret.add_argument("book_id", type=int)

    sub.add_parser("overdue", help="List overdue loans", parents=[common])

    sub.add_parser("notify", help="Email overdue notices", parents=[common])

    p_look = sub.add_parser("lookup", help="Look up a book by ISBN",
                            parents=[common])
    p_look.add_argument("isbn")

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
        print("Run 'python library.py search macbeth' to check it worked.")

    elif args.command == "search":
        catalogue.search(args.term)

    elif args.command == "checkout":
        loans.checkout(args.book_id, args.student_id)

    elif args.command == "return":
        loans.return_book(args.book_id)

    elif args.command == "overdue":
        loans.print_overdue()

    elif args.command == "notify":
        notices.send_overdue_notices(demo=args.demo)

    elif args.command == "lookup":
        catalogue.lookup_isbn(args.isbn, demo=args.demo)

    return 0


if __name__ == "__main__":
    sys.exit(main())
