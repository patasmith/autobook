#!/usr/bin/env python3
import sys
import texteditor
from functools import wraps

from cli.ask import ask_for_action
from cli.utils import has

from typing import Any, Callable


@ask_for_action
def process_string_action(
    action: str, options: dict[str, Callable], default: str
) -> str | bool:
    """Perform an action from the provided options if it exists"""
    action = action.lower() if action else default.lower()
    return options[action]() if action in options else action_not_in_options()


@ask_for_action
def process_bounded_action(
    action: str, options: dict[str, Callable], bounds: range
) -> int | bool:
    """Ensure that the user has entered a bounded number, an available option, or nothing"""
    if action.isdigit():
        number = int(action)
        if bounds.start <= number <= bounds.stop:
            return number
    elif action.lower() in options:
        return options[action.lower()]()
    return action_not_in_options()


def process_action(
    message: str, options: dict[str, Callable], rest: Any
) -> str | int | bool:
    """Process string or bounded action"""
    if type(rest) == str:
        return process_string_action(message, options, rest)
    elif type(rest) == range:
        return process_bounded_action(message, options, rest)


def accept_value(*args) -> bool:
    """Indicates that the user has accepted the value and input is no longer required"""
    return False


def action_not_in_options() -> bool:
    """Indicates that the program should continue to wait for a valid user input"""
    return True


def assign_value(
    fields: dict[str, Any], field: str, value: Any, valid_type: type
) -> Any:
    """Assign a value if it exists and is the right type for assigning, otherwise keep the old value"""
    if value is not None and value and isinstance(value, valid_type):
        return value
    else:
        return fields[field] if has(fields, field) else None


def value_accepted(value: Any) -> bool:
    """Check if a value has been accepted by the user"""
    return value == accept_value()


def quit_program(*args) -> None:
    """Quit the program"""
    print("Quitting...")
    sys.exit()


def display_help(help_text) -> bool:
    """Print help text"""
    print(help_text)
    return True


def edit_value(fields: dict[str, Any], field: str) -> str:
    """Create or edit a value"""
    return (
        texteditor.open(fields[field]).strip()
        if has(fields, field)
        else texteditor.open().strip()
    )


def make_options(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(fields, field, *args, **kwargs):
        options = {}
        help_text = ""
        functions = func(*args, **kwargs)
        for option, function, help in functions:
            options[option] = lambda function=function: function(fields, field)
            display_option = option if option else "<press enter>"
            help_text += display_option + " - " + help + "\n"
        help_text += "? - display command help\nq - exit the program"
        options["?"] = lambda *_: display_help(help_text)
        options["q"] = lambda *_: quit_program()
        return options

    return wrapper


@make_options
def GE_options(generate_value: Callable) -> list[tuple[str, Callable, str]]:
    return [
        ("g", generate_value, "generate new content by sending a request to the AI"),
        ("e", edit_value, "edit content by opening a text editor"),
    ]


@make_options
def YEG_options(generate_value: Callable) -> list[tuple[str, Callable, str]]:
    return [
        ("y", accept_value, "accept the current content"),
        ("g", generate_value, "generate new content by sending a request to the AI"),
        ("e", edit_value, "edit content by opening a text editor"),
    ]


def provide_options(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(fields: dict[str, Any], field: str, generate_value: Callable) -> Any:
        message, options, default = func()
        message = message.format(field, fields[field] if has(fields, field) else None)
        options = options(fields, field, generate_value)
        return process_action(message, options, default)

    return wrapper


def update_field(valid_type: type) -> Callable:
    """Ask user to create or confirm a field's value"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(fields: dict[str, Any], field: str, *args, **kwargs) -> None:
            while True:
                value = func(fields, field, *args, **kwargs)
                fields[field] = assign_value(fields, field, value, valid_type)
                if value_accepted(value):
                    break

        return wrapper

    return decorator


def generate_or_edit(generate: Callable, edit: Callable) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(fields, field, rest):
            edit_value, condition = func(fields, field, rest)
            return (
                edit(fields, field, edit_value)
                if condition
                else generate(fields, field, rest)
            )

        return wrapper

    return decorator
