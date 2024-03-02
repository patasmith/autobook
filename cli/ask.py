#!/usr/bin/env python3
from functools import wraps

from typing import Any, Callable


def make_bound_options_template(template: str, bounds: range) -> str:
    return (
        "(enter a number from {} to {}) ".format(bounds.start, bounds.stop) + template
    )


def make_menu_options_template(template: str, default: str) -> str:
    return template + " (default {})".format(default)


def make_options_template(default: str | range) -> str:
    """Create template for displaying available options"""
    template = "({})"
    if type(default) == range:
        template = make_bound_options_template(template, default)
    elif not default.isalpha():
        template = make_menu_options_template(template, default)
    return template


def make_options_list(options: dict[str, Callable], default: str | range) -> list:
    """Create a list of the available options"""
    options_list = [x for x in list(options.keys()) if x]
    if type(default) == str:
        options_list.remove(default)
        options_list.insert(0, default.upper())
    return options_list


def format_options(options: dict[str, Callable], default: str) -> str:
    """Display available options in a specific format

    The default option will be displayed uppercase if it's a letter,
    or separately if it's not a letter
    """
    template = make_options_template(default)
    options_list = make_options_list(options, default)
    return template.format("/".join(options_list)) + ": "


def make_message(message: str, options: dict[str, Callable], default: str) -> str:
    """Create a message that asks a user for input"""
    return message + " " + format_options(options, default)


def ask_for_action(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(message: str, options: dict[str, Callable], *rest) -> Any:
        action = input(make_message(message, options, *rest))
        return func(action, options, *rest)

    return wrapper
