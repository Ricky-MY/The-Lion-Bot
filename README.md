# The Lion

[![discord.py](https://img.shields.io/pypi/pyversions/discord.py.svg)](https://pypi.python.org/pypi/discord.py)
[![pypi](https://img.shields.io/pypi/v/discord.py.svg)](https://pypi.python.org/pypi/discord.py)

## Table of Contents
* 1. [General Info](#general-info)
* 2. [Bot Explanation](#explanation)
* 3. [Installation](#installation)

### General Info
Multi-purposed discord bot authored in the python language that consists of features such as;  Moderation Commands, Fully text-customizable Welcoming system, Text embed creator / announcing commands (beautifies your announcements), Games and fun commands, Tags and global tags, Over 10 miscellaneous commands and etc...

### Explanation 
**=** Commands In Cogs
Commands that shares a similar purpose are collected in a cog that is named appropriately within (*./bot*)


### Installation
To run this project, install it locally by following these steps:

* 1. Install the discord.py module (USE PYTHON 3.8 OR ABOVE)

You can get the library directly from PyPI:
On macOS:
```
python3 -m pip install -U discord.py
```
If you are using Windows, then the following should be used instead:
```
py -3 -m pip install -U discord.py
```

* 2. Install the menus extension of the discord.py module
```
py -3 -m pip install -U git+https://github.com/Rapptz/discord-ext-menus
```
If you don't have git, make sure to install it before the menus extension.

* 3. Setup dotenv for token feeding

a. Install python-dotenv
macOS:
```
python3 -m pip install python-dotenv
```
Windows:
```
py -3 -m pip install python-dotenv
```
b. Create a `.env` file in the root directory
This must be in the same directory as `__main__.py`

d. Insert in your token
~~~
TOKEN="YOUR_TOKEN"
~~~