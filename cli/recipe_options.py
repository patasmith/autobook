#!/usr/bin/env python3
from autobook.main import outline_to_chapters
from cli.utils import has

from typing import Any


def save_outline_to_chapters(fields: dict[str, Any], field: str) -> None:
    """After creating and confirming an outline, transform it into a chapters structure"""
    if not has(fields, "chapters"):
        fields["chapters"] = outline_to_chapters(fields["outline"])
