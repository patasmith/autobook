#!/usr/bin/env python3
import os
import pytest
from pathlib import Path
from autobook.database import (
    add_book,
    all_books,
    get_book,
    update_book,
    delete_book,
    delete_book_field,
    unfinished_books,
)


def delete_test_db():
    """Helper to delete test db file"""
    test_db_path = Path("instance/test_db.json")
    if test_db_path.exists():
        test_db_path.unlink()


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    """Specify test database name via environment variable
    Remove test database and helper environment variable at end of test
    """
    os.environ["AUTOBOOK_DB_FILENAME"] = "test_db"
    yield
    del os.environ["AUTOBOOK_DB_FILENAME"]
    delete_test_db()


def test_add_book():
    book_id = add_book({"title": "Test Book", "author": "Test Author"})
    assert book_id is not None, "Failed to add book"


def test_get_book():
    book_id = add_book({"title": "Specific Book", "author": "Specific Author"})
    book = get_book(book_id)
    assert book["title"] == "Specific Book", "Get book returned the wrong book"


def test_all_books():
    initial_count = len(all_books())
    add_book({"title": "Another Book", "author": "Another Author"})
    assert (
        len(all_books()) == initial_count + 1
    ), "All books did not return all added books"


def test_update_book():
    book_id = add_book({"title": "Book to Update", "author": "Author A"})
    update_book(book_id, "title", "Updated Title")
    updated_book = get_book(book_id)
    assert updated_book["title"] == "Updated Title", "Book title was not updated"


def test_delete_book():
    book_id = add_book({"title": "Book to Delete", "author": "Author B"})
    delete_book(book_id)
    assert get_book(book_id) is None, "Book was not deleted"


def test_delete_book_field():
    book_id = add_book(
        {"title": "Book with Extra", "author": "Author C", "extra_field": "Extra"}
    )
    delete_book_field(book_id, "extra_field")
    book_after_deletion = get_book(book_id)
    assert "extra_field" not in book_after_deletion, "Book field was not deleted"


def test_unfinished_books():
    book_id = add_book({"title": "Unfinished Book"})
    unfinished_book_list = unfinished_books()
    assert any(
        book["book_id"] == book_id for book in unfinished_book_list
    ), "Unfinished book not detected"
