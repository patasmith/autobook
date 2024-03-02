#!/usr/bin/env python3
import openai
from openai import OpenAI
import os
import re

from autobook.prompts import prompts

from typing import Any

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def get_response(prompt, logit_bias={}, history=None):
    """Send a prompt to the OpenAI chat-based API
    and return the content of the response
    """
    print(
        f"Sending this prompt:\n--------------------\n{prompt}\n--------------------\n"
    )
    print("Waiting for response...")

    messages = [{"role": "user", "content": prompt}]
    if history:
        messages = history + messages
    while True:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo-16k", messages=messages, logit_bias=logit_bias, n=1
            )
            break
        except openai.Timeout as e:
            # Handle timeout error, e.g. retry or log
            print(f"OpenAI API request timed out: {e}")
            pass
        except openai.APIError as e:
            # Handle API error, e.g. retry or log
            print(f"OpenAI API returned an API Error: {e}")
            break
        except openai.APIConnectionError as e:
            # Handle connection error, e.g. check network or log
            print(f"OpenAI API request failed to connect: {e}")
            pass
        except openai.InvalidRequestError as e:
            # Handle invalid request error, e.g. validate parameters or log
            print(f"OpenAI API request was invalid: {e}")
            break
        except openai.AuthenticationError as e:
            # Handle authentication error, e.g. check credentials or log
            print(f"OpenAI API request was not authorized: {e}")
            break
        except openai.PermissionError as e:
            # Handle permission error, e.g. check scope or log
            print(f"OpenAI API request was not permitted: {e}")
            break
        except openai.RateLimitError as e:
            # Handle rate limit error, e.g. wait or log
            print(f"OpenAI API request exceeded rate limit: {e}")
            break

    return response.choices[0].message.content.strip(), response.usage.total_tokens


def generate_content(format_vars: dict, prompt_type: str) -> str:
    """Use a prompt to get some content"""
    formatted_prompt = prompts[prompt_type].format(**format_vars)
    content, tokens = get_response(formatted_prompt)
    return content


def generate_field(fields: dict[str, Any], field: str) -> str:
    if field in fields and fields[field]:
        return fields[field]
    else:
        return generate_content(fields, field)


_is_chapter = r"^[IVXLCDM]+\.\s+"
_is_section = r"^\d+\.\s+"


def get_lines(outline: str) -> list[str]:
    """Return the outline separated into lines, removing empty strings"""
    return [line.strip() for line in outline.strip().split("\n") if line.strip()]


def header_type(regex: str, line: str) -> bool:
    """Used to check if a line is a chapter or section"""
    return re.match(regex, line) is not None


# cannot figure out type hints for this
def string_to_chapters(string: str) -> list[dict[str, Any]]:
    """Return the chapter headers plus associated sections

    Format:
        [ { "header": "I. Chapter 1",
            "sections": [ "1. Section 1",
                          "2. Section 2" ],
            "content": "" },
          { "header": "II. Chapter 2",
            "sections": [ "1. Section 3",
                          "2. Section 4" ],
            "content": "" } ]
    """
    chapters: list[dict[str, Any]] = []
    lines: list[str] = get_lines(string)
    for line in lines:
        if header_type(_is_chapter, line):
            chapters.append({"header": line, "sections": [], "content": ""})
        elif header_type(_is_section, line) and len(chapters) > 0:
            chapters[-1]["sections"].append(line)  # type: ignore

    return chapters


def chapters_to_string(chapters: list) -> str:
    """Return a chapters structure as a single string"""
    string = ""
    for chapter in chapters:
        string += chapter["header"] + "\n"
        for section in chapter["sections"]:
            string += section + "\n"
    return string
