#!/usr/bin/env python3
import datetime
import uuid
from PIL import Image
from dominate.tags import h1, h2, p
from ebooklib import epub


def make_cover_image(width=1600, height=2560, color="white"):
    """Make a blank cover file as a placeholder"""
    print("Creating the image...")
    return Image.new("RGBA", (width, height), color)


def create_chapter_file(content, header, file_name, css_href) -> epub.EpubHtml:
    """Make an xhtml file"""
    # Initialize the file
    xhtml = epub.EpubHtml(title=header, file_name=file_name, lang="en")
    xhtml.add_link(href=css_href, rel="stylesheet", type="text/css")
    # Use the title as the chapter header
    processed_header = h2(header).render()
    # Convert each paragraph in content to HTML, then join together in one string
    processed_content = "".join(
        [p(paragraph).render() for paragraph in content.split("\n")]
    )
    xhtml.content = processed_header + processed_content
    return xhtml


def add_chapter_to_book(book, content, header, file_name, css_href):
    """Add a new chapter to the epub file"""
    # Create a chapter file and add it to the provided book
    xhtml = create_chapter_file(content, header, file_name, css_href)
    book.add_item(xhtml)
    # Save the file name in the provided list
    book.spine.append(xhtml)
    book.toc.append(xhtml)


def add_copyright_page(book, author, css_href):
    """Add a copyright page to the epub file"""
    current_year = datetime.date.today().year
    copyright = (
        f"Copyright © {current_year} by {author}. All rights reserved.\n\n"
        "This book or any portion thereof may not be reproduced or "
        "used in any manner whatsoever without the express written "
        "permission of the publisher except for the use of brief "
        "quotations in a book review."
    )
    page = epub.EpubHtml(title="Copyright", file_name="copyright.xhtml", lang="en")
    lines = copyright.split("\n")
    page.content = "".join(
        [p(paragraph, cls="copyright").render() for paragraph in lines]
    )
    page.add_link(href=css_href, rel="stylesheet", type="text/css")
    book.add_item(page)
    book.spine.append(page)


def add_title_page(book, title, author, css_href):
    """Add a title page to the epub file"""
    page = epub.EpubHtml(title="Title", file_name="title.xhtml", lang="en")
    page.content = (
        h1(title="Title", cls="title").render()
        + h2(author="Author", cls="author").render()
    )
    page.add_link(href=css_href, rel="stylesheet", type="text/css")
    book.add_item(page)
    book.spine.append(page)


def chapters_to_book(
    chapters, title, author, css=None, cover_image=None, file_path="output/book.epub"
):
    """Format book data into an epub"""

    print("Creating ebook...")
    book = epub.EpubBook()

    print("Adding metadata...")
    # Add metadata

    id = uuid.uuid4()
    book.set_identifier(str(id))
    book.set_title(title)
    book.set_language("en")
    book.add_author(author)

    print("Adding cover image...")
    cover = make_cover_image()
    cover.save("cover.png", "PNG")
    with open("cover.png", "rb") as file:
        book.set_cover("cover.png", file.read())
    book.spine.append("cover")

    print("Adding CSS...")
    # Add css file
    css_href = "style/styles.css"
    if css:
        book_css = epub.EpubItem(
            uid="style", file_name=css_href, media_type="text/css", content=css
        )
        book.add_item(book_css)

    print("Adding frontmatter...")
    # Adding title page, copyright page, and so on
    add_title_page(book, title, author, css_href)
    add_copyright_page(book, author, css_href)

    book.spine.append("nav")

    print("Adding chapters...")
    # Add chapters

    for i, chapter in enumerate(chapters):
        add_chapter_to_book(
            book, chapter["content"], chapter["header"], f"chapter{i+1}.xhtml", css_href
        )

    # Add navigation files
    nav = epub.EpubNav()
    nav.add_link(href=css_href, rel="stylesheet", type="text/css")

    book.add_item(epub.EpubNcx())
    book.add_item(nav)

    print("Saving book...")
    # create epub file
    epub.write_epub(file_path, book, {})
    print("Success!")


def load_css(file_path):
    with open(file_path, "r") as file:
        css = file.read()

    return css
