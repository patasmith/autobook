#!/usr/bin/env python3
import argparse

from cli.list_command import list_command
from cli.create_command import create_command
from cli.edit_command import edit_command
from cli.delete_command import delete_command
from cli.export_command import export_command


def add_commands(
    parser: argparse.ArgumentParser, command_data: dict
) -> dict[str, argparse.ArgumentParser]:
    """Add the core commands to the parser"""
    subparsers = parser.add_subparsers(required=True, dest="command")
    command = {}
    for k, v in command_data.items():
        command[k] = subparsers.add_parser(k, help=v)
    return command


def cli() -> None:
    """Generate a book using values from commandline flags"""

    parser = argparse.ArgumentParser(
        description="Generate a book in epub3 format. Also generates the topic, author name, and title if not provided.\n\nFor further help on commands, call the command followed by the -h flag."
    )
    command_data = {
        "list": "List saved books by id and topic. Given a book's id, list the full content for that book.",
        "create": "Create a new book, generating any aspect of the book that is not provided at the command line via flag.",
        "edit": "Edit a saved book with a text editor or by regenerating. By itself, lists incomplete books. With a book id, fills in missing content, or displays list of chapters for easy editing. With a book id and field, edit that content directly.",
        "delete": "Remove a saved book from the database.",
        "export": "Export a saved book to the epub format.",
    }
    command = add_commands(parser, command_data)
    command["create"].add_argument(
        "-c",
        "--category",
        help="Define which type of generation to use (default: nonfiction) Currently only nonfiction is implemented.",
        type=str,
        default="nonfiction",
        const="nonfiction",
        nargs="?",
        choices=["nonfiction"],
    )
    # TODO: consider changing this to "synopsis"
    # the reason would be to make the flag -s
    # then I could more programmatically add arguments...

    # function that just takes name of field, i.e. "subject"
    # and a description and a type
    # and derives "-s", "--synopsis", etc.
    command["create"].add_argument(
        "-o",
        "--topic",
        help='Define the topic of the book, completing the sentence "Write a book about..."',
        type=str,
        required=False,
    )
    command["create"].add_argument(
        "-n",
        "--num_chapters",
        help="Choose the number of chapters to generate.",
        type=int,
        required=False,
    )
    command["create"].add_argument(
        "-a", "--author", help="Define the author's name.", type=str, required=False
    )
    command["create"].add_argument(
        "-t", "--title", help="Define the title of the book.", type=str, required=False
    )
    command["list"].add_argument(
        "book_id",
        help="A valid book id (default: list all books by id and topic).",
        type=int,
        nargs="?",
    )
    command["edit"].add_argument(
        "book_id",
        help="A valid book id (default: list all unfinished books by id and topic).",
        type=int,
        nargs="?",
    )
    command["edit"].add_argument(
        "field",
        help="The field to change (default: resume creation of any missing content in the book).",
        type=str,
        nargs="?",
        choices=["topic", "title", "author", "chapters", "num_chapters", "outline"],
    )
    command["delete"].add_argument("book_id", help="A valid book id.", type=int)
    command["delete"].add_argument(
        "field",
        help="The field to delete.",
        type=str,
        nargs="?",
        choices=["title", "author", "chapters", "num_chapters", "outline"],
    )
    command["export"].add_argument("book_id", help="A valid book id.", type=int)
    command["export"].add_argument("file_path", help="File path for export.")
    command["export"].add_argument(
        "-f",
        "--format",
        help="Define the format for export (default: epub).",
        type=str,
        default="epub",
        const="epub",
        nargs="?",
        choices=["epub", "txt"],
    )

    args = vars(parser.parse_args())
    user_command = args.pop("command")

    commands = {
        "list": list_command,
        "create": create_command,
        "edit": edit_command,
        "delete": delete_command,
        "export": export_command,
    }

    commands[user_command](args)  # type: ignore


if __name__ == "__main__":
    cli()
