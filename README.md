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

* Please change the language in func.py's get_problem_source method for another language. For example, if you want to download java problems change to this: "def get_problem_source(self, problem, language='Java'):". 
> Available languages are 'C++', 'Java', 'Python', 'C', 'C#', 'JavaScript', 'Ruby', 'Swift', 'Go'. (Case sensitive)


### New lc-get command with --overwrite argument:
* lc-get command will skip the process of downloading and overriding specific file content if original file exists. 

- It can help when adding newest problem without losing solutions for old problems.

- Also, it can help with the bad network connection.(For example: if there are HTTP error and therefore unable to dowland the whole repo of problems from leetcode, this command is needed for resuming from break-points by default)

* Whole problem sets can be updated by adding --overwrite argument.
