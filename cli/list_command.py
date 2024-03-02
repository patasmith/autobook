#!/usr/bin/env python3
from pprint import pformat

from autobook.main import list_book, list_books
from cli.utils import list_id_and_topic

from typing import Any


def list_book_content(book: dict) -> None:
    """List formatted content for each field in a book"""
    for key in book:
        content = pformat(book[key])
        print(f"\n{key}:\n{content}")


def list_one(book_id: int) -> None:
    """Pretty-print all info about a single book."""
    book = list_book(book_id)
    if book:
        print(f"Listing book {book_id}...")
        list_book_content(book)


def list_all() -> None:
    """List every book in the database by book id and topic."""
    print("Listing all books...\n")
    list_id_and_topic(list_books())


def list_command(args: dict[str, Any]) -> None:
    """Handle list request"""
    list_one(args["book_id"]) if args["book_id"] else list_all()
