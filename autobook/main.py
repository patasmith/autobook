#!/usr/bin/env python3
from autobook import book, epub, text
from autobook import database as db
from typing import Any


def list_book(book_id: int) -> dict[str, Any]:
    """Return every field of a single book in the database."""
    try:
        return dict(db.get_book(book_id))
    except TypeError as e:
        if "NoneType" in str(e):
            print(
                f"main.list_book: error: argument book_id: book_id {book_id} not found"
            )
        return {}


def simple_list_of_books(raw_books: list) -> list:
    """Given a list of books, return a list of their ids and topics."""
    return [{"id": book["book_id"],
             "topic": book["topic"]} for book in raw_books]


def list_books() -> list[dict[str, Any] | None]:
    """Return the id and topic for every book in the database."""
    return simple_list_of_books(db.all_books())


def list_unfinished_books() -> list[dict[str, Any] | None]:
    """Return every unfinished book in the database."""
    return simple_list_of_books(db.unfinished_books())


def create_book(fields: dict[str, Any]) -> int:
    """Initialize a basic book with provided fields."""
    book_id = db.add_book(fields)
    return book_id


def random_topic() -> str:
    """Generate a random topic for a book."""
    return book.generate_content({}, "topic")


def generate_field_content(fields: dict[str, Any], field: str) -> str:
    """Generate content for a book's field."""
    return book.generate_content(fields, field)


def chapters_to_outline(chapters: list[dict[str, Any]]) -> str:
    """Convert a chapters structure to an outline for viewing."""
    return book.chapters_to_string(chapters)


def outline_to_chapters(outline: str) -> list:
    """Convert an outline to a chapters structure."""
    return book.string_to_chapters(outline)


def load_from_book(book_id: int, field: str) -> str:
    """Grab specific data from a book."""
    book = db.get_book(book_id)
    return book[field]


def save_to_book(book_id: int, field: str, content: str) -> None:
    """Save content to a book."""
    db.update_book(book_id, field, content)


def delete_book(book_id: int) -> None:
    """Delete a book from the database."""
    db.delete_book(book_id)


def delete_book_field(book_id: int, field: str) -> None:
    """Delete a single field of a book."""
    db.delete_book_field(book_id, field)


def export_book_to_epub(book_id: int, file_path: str) -> None:
    """Export a book to an epub file."""
    book = db.get_book(book_id)
    css = epub.load_css("styles/wendy.css")
    epub.chapters_to_book(
        chapters=book["chapters"],
        title=book["title"],
        author=book["author"],
        css=css,
        file_path=file_path,
    )


def export_book_to_text(book_id: int, file_path: str) -> None:
    """Export a book to a text file."""
    book = db.get_book(book_id)
    text.chapters_to_text(
        chapters=book["chapters"],
        title=book["title"],
        author=book["author"],
        file_path=file_path,
    )
