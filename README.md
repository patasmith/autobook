# AutoBook
An ebook generator.

## To run

### Setup
Add your OpenAI API key to your environment as `OPENAI_API_KEY`.

### CLI
`./run "Your topic here" n` where n is the number of chapters you'd like.

`./run -h` to see options.

`./run <subcommand> -h` to see options for each command.

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
