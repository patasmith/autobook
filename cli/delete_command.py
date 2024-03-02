#!/usr/bin/env python3
from autobook.main import delete_book, delete_book_field

from typing import Any


def delete_command(args: dict[str, Any]) -> None:
    """Remove a book from the database, or a single field from a book."""
    if args["field"]:
        delete_book_field(args["book_id"], args["field"])
        print(f"Deleted field {args['field']} from book {args['book_id']}.")
    else:
        try:
            delete_book(args["book_id"])
            print(f"Deleted book {args['book_id']}.")
        except KeyError:
            print(f"No book {args['book_id']} in database.")
