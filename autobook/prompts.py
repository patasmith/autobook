#!/usr/bin/env python3

prompts = {
    "topic": (
        "Write a topic for a book. This topic is one sentence long. "
        "Only return the topic, nothing else."
    ),
    "title": (
        "Write a title for a book about {topic}. Only write the title, nothing else."
    ),
    "author": (
        "Write an author name for a book about {topic}. Only write the author name, nothing else."
    ),
    "outline": (
        "Generate a chapter outline for a book titled {title}. It is about {topic}. "
        "It has exactly {num_chapters} chapters. The outline follows the format:\n"
        "I. Chapter\n"
        "1. Section\n"
        "All chapters start with Roman numerals. All sections start with Arabic numerals. "
        "Include a minimum of one section and a maximum of three sections per chapter, your choice. "
        "Generate exactly {num_chapters} chapters, no more and no less."
    ),
    "content": (
        "You have the following outline for a book about {topic}, "
        'written by {author} with the title "{title}":\n\n'
        "{outline}\n\n"
        "Write the full text of {chapter}, expanding on all sections in depth. Start right at the first words, don't include the chapter title."
    ),
    "header": (
        "You have the following outline for a book about {topic}, "
        'written by {author} with the title "{title}":\n\n'
        "{outline}\n\n"
        "Write a new chapter header to replace this chapter header: {chapter}."
    ),
    "sections": (
        "You have the following outline for a book about {topic}, "
        'written by {author} with the title "{title}":\n\n'
        "{outline}\n\n"
        "Write section headers for this chapter header: {chapter}."
    ),
}
