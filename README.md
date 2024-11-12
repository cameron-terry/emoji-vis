What does it look like when you group similar emojis on a 2D graph

# dev stuff
## v0
in `v0`, run `source dev_setup.sh`. This installs a code linter [ruff](https://github.com/astral-sh/ruff) for pre-commit checks

### testing
`coverage run -m pytest  -v -s && coverage report -m` for unit tests
coverage must be above 0.9

[excluding code coverage](https://coverage.readthedocs.io/en/latest/excluding.htmlhttps://coverage.readthedocs.io/en/latest/excluding.html)
