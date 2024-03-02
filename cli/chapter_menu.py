#!/usr/bin/env python3
from autobook.main import chapters_to_outline, generate_field_content
from cli.inputs import make_options, process_action
from cli.menus import (
    C_options,
    generate_or_edit_menu_value,
    menu_command,
    run_menu,
    select_field_index,
)

from typing import Any, Callable


def make_chapter_format_args(
    fields: dict[str, Any], field: str, additional_args: dict[str, str]
) -> dict[str, Any]:
    """Expand fields with additional entries used for formatting prompts"""
    temp_fields = {
        "topic": fields["topic"],
        "author": fields["author"],
        "title": fields["title"],
        "outline": chapters_to_outline(fields[field]),
    }
    return dict(temp_fields, **additional_args)


def update_chapter_by_index(
    fields: dict[str, Any], field: str, field_index: int, key: str
) -> None:
    """Access a chapter at a specific index and update one of its values"""
    chapter = fields[field][field_index]
    to_update = chapter
    format_args = make_chapter_format_args(
        fields, field, {"chapter": chapter["header"]}
    )
    if type(chapter[key]) == list:
        to_update = {key: "\n".join(chapter[key])}
    generate_or_edit_menu_value(
        to_update, key, lambda *_: generate_field_content(format_args, key)
    )
    if type(chapter[key]) == list:
        chapter[key] = to_update[key].split("\n")


def select_chapter_index(fields: dict[str, Any], field: str, info: str) -> int | bool:
    """Return the index of a specific chapter in the chapters list"""
    info = " to " + info if info else ""
    select_message = "Select a chapter{}".format(info)
    return select_field_index(
        select_message,
        len(fields[field]),
        C_options(fields, ""),
    )


def find_next_unwritten_chapter(fields: dict[str, Any], field: str) -> int | bool:
    """Return the index of the next unwritten chapter"""
    for i, chapter in enumerate(fields[field]):
        if not chapter["content"]:
            # adding one here because select_field_index, which this is used as a lambda for, subtracts one
            return i + 1
    return True


def select_chapter_or_next_unwritten_chapter(
    fields: dict[str, Any], field: str, info: str
) -> int | bool:
    """Return the index of a specific chapter in the chapters list"""
    info = " to " + info if info else ""
    select_message = "Select a chapter{}, or press <enter> to select the next unwritten chapter".format(
        info
    )
    return select_field_index(
        select_message,
        len(fields[field]),
        C_options(
            fields,
            "",
            lambda *_: find_next_unwritten_chapter(fields, field),
            "select next unwritten chapter",
        ),
    )


def select_chapter_destination(
    fields: dict[str, Any], field: str, _: Any
) -> int | bool:
    """Return the index of a specific chapter in the chapters list"""
    return select_field_index(
        "Select chapter destination, or press <enter> to add to end",
        len(fields[field]),
        # we are adding 1 here to compensate for select_field_index subtracting 1 from everything, which is not necessary when it comes to a length
        C_options(fields, "", lambda *_: len(fields[field]) + 1, "add to end"),
    )


def insert_new_chapter(fields: dict[str, Any], field: str, field_index: int) -> None:
    """Insert a chapter into the chapters list, pushing other chapters up"""
    fields[field].insert(
        field_index,
        {"header": "<new chapter>", "sections": ["<new sections>"], "content": ""},
    )


@menu_command(select_chapter_or_next_unwritten_chapter, "add/edit content")
def add_chapter_content(fields: dict[str, Any], field: str, field_index: int) -> bool:
    """Choose a chapter and update its content"""
    update_chapter_by_index(fields, field, field_index, "content")


@menu_command(select_chapter_index, "edit the header/sections")
def edit_chapter_header_and_sections(
    fields: dict[str, Any], field: str, field_index: int
) -> bool:
    """Choose a chapter and update its header and sections"""
    update_chapter_by_index(fields, field, field_index, "header")
    update_chapter_by_index(fields, field, field_index, "sections")


@menu_command(select_chapter_destination, "")
def add_new_chapter(fields: dict[str, Any], field: str, field_index: int) -> bool:
    """Add a new chapter"""
    insert_new_chapter(fields, field, field_index)
    update_chapter_by_index(fields, field, field_index, "header")
    update_chapter_by_index(fields, field, field_index, "sections")


@menu_command(select_chapter_index, "move")
def move_chapter(fields: dict[str, Any], field: str, field_index: int) -> bool:
    """Move a chapter"""

    @menu_command(select_chapter_destination, "")
    def move_to(
        fields: dict[str, Any], field: str, destination_field_index: int
    ) -> bool:
        fields[field].insert(destination_field_index, fields[field].pop(field_index))

    move_to(fields, field, "")


@menu_command(select_chapter_index, "delete")
def delete_chapter(fields: dict[str, Any], field: str, field_index: int) -> bool:
    """Delete a chapter"""
    # TODO: seems to be defaulting to Y if anything garbage is entered
    confirm = process_action(
        "Confirm delete chapter {}?".format(field_index + 1),
        {"y": lambda *_: True, "n": lambda *_: False},
        "n",
    )
    if confirm:
        del fields[field][field_index]


@menu_command(select_chapter_index, "delete content only")
def delete_chapter_content(
    fields: dict[str, Any], field: str, field_index: int
) -> bool:
    """Delete a chapter's content"""
    confirm = process_action(
        "Confirm delete content of chapter {}?".format(field_index + 1),
        {"y": lambda *_: True, "n": lambda *_: False},
        "n",
    )
    if confirm:
        fields[field][field_index]["content"] = ""


chapter_menu_commands = [
    (
        "Add/edit chapter content",
        add_chapter_content,
        "Select a chapter to add its content if it is marked unwritten, or edit its existing content",
    ),
    (
        "Edit chapter header and sections",
        edit_chapter_header_and_sections,
        "Select a chapter to change its header and sections through generation or editing",
    ),
    (
        "Add new chapter",
        add_new_chapter,
        "Select a spot to insert a new chapter, or add one to the end of the book",
    ),
    (
        "Move existing chapter",
        move_chapter,
        "Select a chapter to move it to another place in the book",
    ),
    (
        "Delete chapter",
        delete_chapter,
        "Select a chapter to delete it entirely (cannot undo once confirmed)",
    ),
    (
        "Delete chapter content",
        delete_chapter_content,
        "Select a chapter to delete only its content, leaving the header and sections untouched",
    ),
]


def format_chapters(chapters: list[dict[str, Any]]) -> str:
    content = "\n"
    for i, chapter in enumerate(chapters):
        content += "[{}] {}".format(i + 1, chapter["header"])
        if not chapter["content"]:
            content += " (unwritten)"
        content += "\n"
        for section in chapter["sections"]:
            content += "\t{}\n".format(section)
    return content


def run_chapter_menu(fields: dict[str, Any], field: str) -> str | bool:
    return run_menu(fields, field, chapter_menu_commands, format_chapters)
