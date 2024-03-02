# AutoBook
An ebook generator in development.

You can:
- Create books
- Generate and edit book content
- Store books in a simple JSON database file
- Export books to text or epub

All books are generated using a simple outline structure. Prompts are naive: individual chapters will reflect content of outline but not content of other chapters.

## To run

### Setup
Clone or fork this repository.

Add your OpenAI API key to your environment as `OPENAI_API_KEY`.

Model and parameters are hardcoded (for now) in `autobook/book.py`.

### CLI
`./run -h` to see available subcommands.

`./run <subcommand> -h` to see options for each command.

#### Examples

`./run create` to make your first book.

`./run create -o "apples" -n 5` to begin creating a 5-chapter book about apples.

`./run list` to view all created books.

`./run export -f epub 1 apples.epub` to export the book with book_id 1 using the epub format.

## Development notes

### Actions
- Run the program on the command line: `./run`
- Call tests: `./test`
- Find anything marked `TODO`: `./todo`
- Verify type checking: `mypy .`
- Clean up formatting: `black .`

### Virtual environment:
- Install: `python -m venv venv` in the root folder
- Activate: `source venv/bin/activate`
- Deactivate: `deactivate`
- Freeze pip requirements: `pip freeze -l > requirements.txt`
- Install pip requirements: `pip install -r requirements.txt`

## Contributor notes

### Workflow:
Follow [Github-flow](https://githubflow.github.io/).

#### Add a new feature
- Update main: `git checkout main; git pull`
- Start a new branch: `git checkout -b new-branch`
- Work on the branch: `git commit -m message`

#### Merge when new feature is complete
- Add the branch to the Github repo: `git push origin new-branch`
- Go to the repo's webpage and initiate a pull request for the new branch
- Document branch changes in the pull request
- Wait for approval or merge immediately

#### Post-merge cleanup
- Once merged, delete branch on Github
- Delete locally if you're done with the branch: `git branch -d new-branch`
- If you're still working on the branch locally, rebase with main (only do this for personal branches)
  - [Rebase instructions](https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/How-to-Git-rebase-a-branch-to-master-example)
  - Switch to main and update: `git checkout main; git pull`
  - Since branch and main are now in alignment, have them split off at the current point: `git rebase main new-branch`

### Standards
- Type hints: [mypy cheatsheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
- Style guide: [PEP 8](https://peps.python.org/pep-0008/) ([*Black*](https://pypi.org/project/black/) should take care of this automatically)
