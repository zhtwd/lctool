# The command line tool for Leetcode
------------------------------------

## Introduction
---------------
It's a tool to get all problems and organize the source codes with problem contents
into folders according to tags. You can also submit it using command line.

## Installation
---------------
Requirements:
1. Anaconda (recommended) or other python environments
2. pip install BeautifulSoup

Install:
python setup install

## Usage
--------
Use freely all the functions and/or two easy commands (lc-get and lc-submit).
* Please input your own username and password in func.py if you want to use submit functions.
* Please change the language in func.py's get_problem_source method for another language. For example, if you want to download java problems change to this: "def get_problem_source(self, problem, language='Java'):"

Explanation for new lc-get command and its --overwrite argument:
* This command will skip the process of downloading and overriding specific file content if original file exists.
* Therefore it can help when you want to add newest problem without losing your solutions for old problems.
* Also, it can help for people with bad network connection.(Me as an example: always meet HTTP error and therefore unable to dowland the whole repo of problems from leetcode, so I need this command to resume from break-points)
* Please change the file suffixes in run.py's lcrefresh() method for another language. Example:"if os.path.exists(filepath + '.' + 'java'):" is for java.
* If you want to use old lc-get's function, add --overwrite argument, this will update your whole repository.
