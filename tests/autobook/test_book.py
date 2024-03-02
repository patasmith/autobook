import pytest
from autobook.book import (
    generate_content,
    generate_field,
    get_lines,
    string_to_chapters,
    chapters_to_string,
)


@pytest.fixture
def mock_response(mocker):
    # Mocking get_response's return value
    mocker.patch("autobook.book.get_response", return_value=("Mocked Response", 50))
    mocker.patch.dict(
        "autobook.prompts.prompts",
        {"test_field": "fake prompt 1", "test_prompt": "fake prompt 2"},
    )


def test_generate_content(mock_response):
    # Test that generate_content correctly formats and returns mocked content
    content = generate_content({"var1": "Test"}, "test_prompt")
    assert content == "Mocked Response"


def test_generate_field_with_provided_field(mock_response):
    # Test generate_field when field is provided in fields dict
    fields = {"test_field": "Predefined Field Content"}
    field_content = generate_field(fields, "test_field")
    assert field_content == "Predefined Field Content"


def test_generate_field_with_generated_field(mock_response):
    # Test generate_field when field needs to be generated
    fields = {"var1": "Test"}
    field_content = generate_field(fields, "test_field")
    assert field_content == "Mocked Response"


def test_get_lines():
    # Test the get_lines function with a simple outline
    outline = "Line 1\n\nLine 2\nLine 3"
    result = get_lines(outline)
    assert result == ["Line 1", "Line 2", "Line 3"]


def test_string_to_chapters():
    # Test converting a string to chapters structure
    input_string = "I. Chapter 1\n1. Section 1\n2. Section 2\nII. Chapter 2\n1. Section 3\n2. Section 4"
    chapters = string_to_chapters(input_string)
    expected = [
        {
            "header": "I. Chapter 1",
            "sections": ["1. Section 1", "2. Section 2"],
            "content": "",
        },
        {
            "header": "II. Chapter 2",
            "sections": ["1. Section 3", "2. Section 4"],
            "content": "",
        },
    ]
    assert chapters == expected


def test_chapters_to_string():
    # Test converting chapters structure back to a string
    chapters = [
        {
            "header": "I. Chapter 1",
            "sections": ["1. Section 1", "2. Section 2"],
            "content": "",
        },
        {
            "header": "II. Chapter 2",
            "sections": ["1. Section 3", "2. Section 4"],
            "content": "",
        },
    ]
    result_str = chapters_to_string(chapters)
    expected_str = "I. Chapter 1\n1. Section 1\n2. Section 2\nII. Chapter 2\n1. Section 3\n2. Section 4\n"
    assert result_str == expected_str
