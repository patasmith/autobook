#!/usr/bin/env python3
import random

from cli.utils import has
from cli.inputs import (
    accept_value,
    action_not_in_options,
    make_options,
    process_action,
    provide_options,
    update_field,
    generate_or_edit,
)


from typing import Any, Callable


@make_options
def bound_options(bounds: range) -> list[tuple[str, Callable, str]]:
    return [
        (
            "g",
            lambda *_: random.randint(bounds.start, bounds.stop),
            "generate a random number between {} and {}".format(
                bounds.start, bounds.stop
            ),
        )
    ]


def generate_bounded_value(fields, field, bounds: range) -> int | bool:
    """Ask user to generate or edit a bounded value"""
    message = "How many chapters?"
    return process_action(message, bound_options(fields, field, bounds), bounds)


@make_options
def YN_options(reject_value: Callable) -> list[tuple[str, Callable, str]]:
    return [
        ("y", accept_value, "accept the current value"),
        ("n", reject_value, "reject the current value"),
    ]


def reject_value(fields: dict[str, Any], field: str) -> bool:
    return bool(fields.pop(field))


@provide_options
def edit_bounded_value() -> str | bool:
    return "Generate outline with {1} chapters?", YN_options, "y"


@update_field(int)
@generate_or_edit(generate_bounded_value, edit_bounded_value)
def generate_or_edit_bounded_value(
    fields: dict[str, Any], field: str, bounds: range
) -> int | str | bool:
    """Ask user to create/edit a bounded value based on if it exists or not"""
    return reject_value, (has(fields, field) and type(fields[field]) == int)
