#!/usr/bin/env python3
from typing import Any, Optional


def has(fields: dict[str, Any], field: str) -> bool:
    """Check if the field exists and has a non-blank value"""
    return field in fields and fields[field]


def list_id_and_topic(books: Optional[list[Any]]) -> None:
    """Pretty-print id and topic for each book in a list"""
    if books:
        for book in books:
            print(f"id: {book['id']}\ttopic: {book['topic']}")
    else:
        print("No books found.")
