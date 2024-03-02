#!/usr/bin/env python3
from autobook.main import generate_field_content
from cli.inputs import (
    accept_value,
    edit_value,
    make_options,
    process_action,
    provide_options,
    update_field,
    generate_or_edit,
)
from cli.utils import has

from typing import Any, Callable


@make_options
def GEC_options(generate_value: Callable) -> list[tuple[str, Callable, str]]:
    return [
        ("g", generate_value, "generate new content by sending a request to the AI"),
        ("e", edit_value, "edit content by opening a text editor"),
        (
            "c",
            lambda *_: False,
            "cancel the current task and return to the home menu",
        ),
    ]


@make_options
def YEGC_options(generate_value: Callable) -> list[tuple[str, Callable, str]]:
    return [
        ("y", accept_value, "accept the current content"),
        ("g", generate_value, "generate new content by sending a request to the AI"),
        ("e", edit_value, "edit content by opening a text editor"),
        (
            "c",
            lambda *_: False,
            "cancel the current task and return to the home menu",
        ),
    ]


@make_options
def C_options(action=None, message=None) -> list[tuple[str, Callable, str]]:
    options = [
        ("c", lambda *_: False, "cancel the current task and return to the home menu")
    ]
    if action:
        options = [("", action, message)] + options
    return options


@provide_options
def generate_menu_value() -> str | bool:
    """Ask user to generate or edit a value"""
    return "Generate or edit {}?", GEC_options, "g"


@provide_options
def edit_menu_value() -> str | bool:
    """Ask user to accept, generate, or edit a value"""
    return 'Use {} "{}"?', YEGC_options, "y"


@update_field(str)
@generate_or_edit(generate_menu_value, edit_menu_value)
def generate_or_edit_menu_value(fields, field, generate_value):
    return generate_value, has(fields, field)


def select_field_index(
    message: str, list_length: int, commands: dict[str, Any]
) -> int | bool:
    """Return a user-chosen index from a list"""
    bounds = range(1, list_length)
    message = message.format(str(bounds.start), str(bounds.stop))
    value = process_action(message, commands, bounds)
    return value - 1 if type(value) == int else value


def format_command_list(commands: list[tuple[str, Callable]]) -> str:
    """Create a list of available commands"""
    return "\n".join(
        ["{}) {}".format(i + 1, command[0]) for i, command in enumerate(commands)]
    )


def make_menu_message(commands: list[tuple[str, Callable]]) -> str:
    """Create a prompt with a list of available commands"""
    return "{}\nSelect an option".format(format_command_list(commands))


@make_options
def menu_options(
    commands: list[tuple[str, Callable, str]]
) -> list[tuple[str, Callable, str]]:
    """Create a list of selectable options from a list of available commands"""
    return [
        ("{}".format(i + 1), command[1], command[2])
        for i, command in enumerate(commands)
    ]


def display_status(fields: dict[str, Any], field: str, formatter: Callable) -> None:
    """Format a dictionary value"""
    print(formatter(fields[field]))


def run_menu(
    fields: dict[str, Any],
    field: str,
    commands: list[tuple[str, Callable, str]],
    formatter: Callable,
) -> str | bool:
    """Let the user choose an action from a list"""
    options = menu_options(fields, field, commands)
    display_status(fields, field, formatter)
    return process_action(
        make_menu_message(commands),
        options,
        "1",
    )


def menu_command(select_index, info):
    """Decorator for a menu command that operates on an ordered list of dicts

    select_index is the function used to select which object to operate on
    info is the string that is used to communicate to the user what action this command performs
    """

    def decorator(func):
        def wrapper(fields, field):
            while True:
                field_index = select_index(fields, field, info)
                if type(field_index) == int:
                    func(fields, field, field_index)
                    break
                elif not field_index:
                    break
            return True

        return wrapper

    return decorator
