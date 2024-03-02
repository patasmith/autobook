#!/usr/bin/env python3


def chapters_to_text(chapters, title, author, file_path="output/book.txt"):
    with open(file_path, "w") as f:
        f.write(title or "")
        f.write("\n\n")
        f.write(author or "")
        f.write("\n\n\n\n")
        for chapter in chapters:
            f.write(chapter["header"] or "")
            f.write("\n\n")
            f.write(chapter["content"] or "")
            f.write("\n\n\n\n")
    print("Book exported to {}.".format(file_path))
