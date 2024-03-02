import pytest
from autobook import main


@pytest.fixture
def mock_db(mocker):
    # Mock all db interactions to isolate tests from the database
    mocker.patch("autobook.main.db")
    mocker.patch(
        "autobook.main.db.get_book",
        return_value={"book_id": 1, "topic": "Fiction", "content": "lorem ipsum"},
    )
    mocker.patch(
        "autobook.main.db.all_books",
        return_value=[
            {"book_id": 1, "topic": "Fiction"},
            {"book_id": 2, "topic": "Non-Fiction"},
        ],
    )
    mocker.patch(
        "autobook.main.db.unfinished_books",
        return_value=[{"book_id": 1, "topic": "Fiction"}],
    )
    mocker.patch("autobook.main.db.add_book", return_value=3)
    mocker.patch("autobook.main.db.update_book")
    mocker.patch("autobook.main.db.delete_book")
    mocker.patch("autobook.main.db.delete_book_field")
    mocker.patch("autobook.main.book")
    mocker.patch("autobook.main.book.generate_content", return_value="lorem ipsum")


def test_list_book_found(mock_db):
    book = main.list_book(1)
    assert book == {"book_id": 1, "topic": "Fiction", "content": "lorem ipsum"}


def test_list_book_not_found(mocker, capsys):
    mocker.patch("autobook.main.db.get_book", return_value=None)
    book = main.list_book(999)
    captured = capsys.readouterr()
    assert book == {}
    assert "book_id 999 not found" in captured.out


def test_simple_list_of_books(mock_db):
    books = main.simple_list_of_books(
        [{"book_id": 1, "topic": "Fiction"}, {"book_id": 2, "topic": "Non-Fiction"}]
    )
    assert books == [{"id": 1, "topic": "Fiction"}, {"id": 2, "topic": "Non-Fiction"}]


def test_list_books(mock_db):
    books = main.list_books()
    assert books == [{"id": 1, "topic": "Fiction"}, {"id": 2, "topic": "Non-Fiction"}]


def test_list_unfinished_books(mock_db):
    books = main.list_unfinished_books()
    assert books == [{"id": 1, "topic": "Fiction"}]


def test_create_book(mock_db):
    book_id = main.create_book({"title": "New Book", "content": "Some content"})
    assert book_id == 3


def test_generate_field_content(mock_db):
    content = main.generate_field_content({"book_id": 1, "topic": "Fiction"}, "content")
    assert content == "lorem ipsum"


def test_load_from_book(mock_db):
    content = main.load_from_book(1, "content")
    assert content == "lorem ipsum"


def test_save_to_book(mock_db):
    main.save_to_book(1, "content", "new content")
    main.db.update_book.assert_called_once_with(1, "content", "new content")


def test_delete_book(mock_db):
    main.delete_book(1)
    main.db.delete_book.assert_called_once_with(1)


def test_delete_book_field(mock_db):
    main.delete_book_field(1, "content")
    main.db.delete_book_field.assert_called_once_with(1, "content")
