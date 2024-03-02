#!/usr/bin/env python3
from autobook.main import export_book_to_epub, export_book_to_text, list_book
from cli.utils import has

from typing import Any


def export_command(args: dict[str, Any]) -> None:
    """Export a saved book to epub format"""
    print("Exporting a saved book...")
    book_id = args["book_id"]
    file_path = args["file_path"]
    fields = list_book(book_id) or {}
    if has(fields, "chapters"):
        if args["format"] == "txt":
            export_book_to_text(book_id, file_path)
        else:
            export_book_to_epub(book_id, file_path)
    else:
        print("Book does not have any saved chapters yet.")
