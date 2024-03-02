#!/usr/bin/env python3
from autobook.main import save_to_book, generate_field_content
from cli.string_options import generate_or_edit_value
from cli.bound_options import generate_or_edit_bounded_value
from cli.recipe_options import save_outline_to_chapters
from cli.utils import has
from cli.chapter_menu import run_chapter_menu

from typing import Any, Callable


required_fields: dict[str, Any] = {
    "topic": {"type": "string"},
    "title": {"type": "string"},
    "author": {"type": "string"},
    "num_chapters": {"type": "bound", "bounds": (3, 20)},
    "outline": {"type": "string"},
    "outline_to_chapters": {
        "type": "recipe",
        "recipe": save_outline_to_chapters,
        "save_to": "chapters",
    },
    "chapters": {"type": "menu", "menu": run_chapter_menu},
}

field_orders: dict[str, list[str]] = {
    "nonfiction": [
        "title",
        "author",
        "num_chapters",
        "outline",
        "outline_to_chapters",
        "chapters",
    ],
}


def save_at_end(fields, field, generator: Callable, *rest) -> None:
    """Generate information and save at the end"""
    generator(fields, field, *rest)
    save_to_book(fields["book_id"], field, fields[field])


def save_at_each_step(fields, field, generator: Callable, *rest) -> None:
    """Generate information and save at the end"""
    while generator(fields, field, *rest):
        save_to_book(fields["book_id"], field, fields[field])


def make_field_generator(
    fields: dict[str, Any], field: str, **rest
) -> tuple[str, Callable]:
    """Create a generator for a basic field in a book"""
    return (
        field,
        lambda: save_at_end(
            fields, field, generate_or_edit_value, generate_field_content
        ),
    )


def make_bounded_field_generator(
    fields: dict[str, Any], field: str, bounds: range, **rest
) -> tuple[str, Callable]:
    """Create a generator for a bounded numerical field in a book"""
    return (
        field,
        lambda: save_at_end(
            fields, field, generate_or_edit_bounded_value, range(*bounds)
        ),
    )


def make_recipe_generator(
    fields: dict[str, Any], field: str, recipe: Callable, save_to: str, **rest
) -> tuple[str, Callable]:
    """Create a generator that alters multiple fields"""
    return (
        field,
        lambda: save_at_end(fields, save_to, recipe),
    )


def make_menu_generator(
    fields: dict[str, Any], field: str, menu: Callable, **rest
) -> tuple[str, Callable]:
    """Create a generator for a menu that alters a complex field"""
    if not has(fields, field):
        fields[field] = []
    return (field, lambda: save_at_each_step(fields, field, menu))


generators: dict[str, Callable] = {
    "string": make_field_generator,
    "bound": make_bounded_field_generator,
    "recipe": make_recipe_generator,
    "menu": make_menu_generator,
}


def make_generator(fields: dict[str, Any], field: str) -> tuple[str, Callable]:
    return generators[required_fields[field]["type"]](
        fields, field, **required_fields[field]
    )


def make_generators(fields: dict[str, Any]) -> list[tuple[str, Callable]]:
    """Create a list of generators according to the order of fields in a book"""
    return [make_generator(fields, field) for field in field_orders[fields["category"]]]


def run_generator(generator: tuple[str, Callable], fields: dict[str, Any]) -> None:
    """Generate and save content for a single field using its generator"""
    generator[1]()


def populate_field(generator: tuple[str, Callable], fields: dict[str, Any]) -> None:
    """Generate unwrtten field content for a book"""
    field = generator[0]
    if (
        (has(required_fields[field], "save_to") and not has(fields, "save_to"))
        or not has(fields, field)
        or required_fields[field]["type"] == "menu"
    ):
        run_generator(generator, fields)


def open_book(fields: dict[str, Any], parser: Callable) -> None:
    """Generate a book by applying a function to each field that's supposed to be in it"""
    generators = make_generators(fields)
    for generator in generators:
        parser(generator, fields)


def continue_book(fields: dict[str, Any]) -> None:
    """Generate a book, skipping fields that are already present"""
    open_book(fields, populate_field)


def start_book(fields: dict[str, Any]) -> None:
    """Generate a book, confirming each field that's present"""
    open_book(fields, run_generator)
