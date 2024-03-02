#!/usr/bin/env python3
from autobook.main import list_book, list_unfinished_books
from cli.generators import continue_book, make_generator, run_generator
from cli.utils import list_id_and_topic

from typing import Any


def edit_field(args: dict[str, Any]) -> None:
    """Edit the content of a book's field."""
    print("Editing a saved book...")
    book_id = args["book_id"]
    fields = list_book(book_id)
    field = args["field"]
    run_generator(make_generator(fields, field), fields)


def list_all_unfinished_books() -> None:
    """List all unfinished books"""
    print("Unfinished books:\n")
    list_id_and_topic(list_unfinished_books())


def resume_editing(args: dict[str, Any]) -> None:
    """Edit a specific book's field or start at next required field for category"""
    try:
        edit_field(args) if args["field"] else continue_book(list_book(args["book_id"]))
    except KeyError:
        print(f"No book {args['book_id']} in database.")


def edit_command(args: dict[str, Any]) -> None:
    """Edit a specific book or list books that need editing"""
    resume_editing(args) if args["book_id"] else list_all_unfinished_books()
