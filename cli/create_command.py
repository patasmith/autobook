#!/usr/bin/env python3
import texteditor

from autobook.main import random_topic, create_book, list_book
from cli.generators import start_book
from cli.string_options import generate_or_edit_value

from typing import Any


def initialize_book(fields: dict[str, Any]) -> int:
    """Generate a topic for a new book and add it to the database"""
    generate_or_edit_value(fields, "topic", lambda *args: random_topic())
    print(f"Creating new book with topic: {fields['topic']}...")
    book_id = create_book(fields)
    print(f"Book created with id {book_id}.")
    return book_id


def create_command(args: dict[str, Any]) -> None:
    """Create a new book"""
    print("Creating a new book...")
    book_id = initialize_book(args)
    fields = list_book(book_id)
    start_book(fields)
