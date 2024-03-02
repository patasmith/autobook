#!/usr/bin/env python3
from cli.inputs import (
    GE_options,
    provide_options,
    update_field,
    YEG_options,
    generate_or_edit,
)
from cli.utils import has

from typing import Any, Callable


@provide_options
def generate_string_value() -> str | bool:
    """Ask user to generate or edit a value"""
    return "Generate or edit {}?", GE_options, "g"


@provide_options
def edit_string_value() -> str | bool:
    """Ask user to accept, generate, or edit a value"""
    return 'Use {} "{}"?', YEG_options, "y"


@update_field(str)
@generate_or_edit(generate_string_value, edit_string_value)
def generate_or_edit_value(
    fields: dict[str, Any], field: str, generate_value: Callable
) -> str | bool:
    """Ask user to create/edit a value based on if it exists or not"""
    return generate_value, has(fields, field)
