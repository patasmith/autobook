#!/usr/bin/env python3
import os
from functools import wraps
from pathlib import Path
from tinydb import TinyDB, Query, where
from tinydb.operations import delete
from tinydb.table import Document

from tinydb.queries import QueryInstance
from typing import Callable


def init_db(table_name: str) -> Callable:
    """Decorator function to initialize the database.

    Database will be stored in instance/db.json by default.
    Set AUTOBOOK_DB_FILENAME in your environment to change the filename.

    @init_db(table_name): the following function will interact with the desired table
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            file_name = os.environ.get("AUTOBOOK_DB_FILENAME", "db")
            Path("instance").mkdir(parents=True, exist_ok=True)
            db = TinyDB(f"instance/{file_name}.json")
            table = db.table(table_name)
            return func(table, *args, **kwargs)

        return wrapper

    return decorator


@init_db("book")
def add_book(db, fields: dict) -> int:
    """Add a book to the database."""
    return db.insert(fields)


def add_doc_ids(books: list[Document]) -> list[Document]:
    """Add doc ids to a list of books"""
    for book in books:
        book["book_id"] = book.doc_id
    return books


@init_db("book")
def all_books(db) -> list[Document]:
    """Return every book in the database."""
    return add_doc_ids(db.all())


def unfinished_field(field: str) -> QueryInstance:
    """Return a query which filters for a field not existing, or having a None or empty string value"""
    return (where(field).one_of([None, ""])) | ~(where(field).exists())


# TODO: so this is intended to return books that are not "finished", as in not all their applicable fields are filled in
# however, it is only deciding this based on these three fields...
# Perhaps books should have a finished flag set on completion
# Perhaps books should simply be listed with their present flags
# Or perhaps the concept of a finished book is flawed in the first place
# Something to decide for the future
@init_db("book")
def unfinished_books(db) -> list[Document]:
    """Return the books that don't have all the necessary fields for export."""
    return add_doc_ids(
        db.search(
            unfinished_field("title")
            | unfinished_field("author")
            | unfinished_field("chapters")
        )
    )


@init_db("book")
def get_book(db, book_id: int) -> Document | None:
    """Get a single book from the database."""
    book = db.get(doc_id=book_id)
    if book is not None:
        book["book_id"] = book_id
    return book


@init_db("book")
def update_book(db, book_id: int, field: str, content: str) -> None:
    """Update a field of a book in the database."""
    db.update({field: content}, doc_ids=[book_id])


@init_db("book")
def delete_book(db, book_id: int) -> None:
    """Remove a book from the database."""
    db.remove(doc_ids=[book_id])


@init_db("book")
def delete_book_field(db, book_id: int, field: str) -> None:
    """Remove a book from the database."""
    book = db.get(doc_id=book_id)
    if field in book:
        db.update(delete(field), doc_ids=[book_id])
