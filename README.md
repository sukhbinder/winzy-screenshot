# winzy-screenshot

[![PyPI](https://img.shields.io/pypi/v/winzy-screenshot.svg)](https://pypi.org/project/winzy-screenshot/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/winzy-screenshot?include_prereleases&label=changelog)](https://github.com/sukhbinder/winzy-screenshot/releases)
[![Tests](https://github.com/sukhbinder/winzy-screenshot/workflows/Test/badge.svg)](https://github.com/sukhbinder/winzy-screenshot/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/winzy-screenshot/blob/main/LICENSE)

Screenshot using python 

## Installation

First configure your Winzy project [to use Winzy](https://github.com/sukhbinder/winzy).

Then install this plugin in the same environment as your Winzy application.
```bash
pip install winzy-screenshot
```
## Usage

To use

```bash
winzy screenshot -b 7.57 8.11 70.14 51.0
```

![winzy screenshot demo](winzy-screenshot-demo.gif)


## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd winzy-screenshot
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
