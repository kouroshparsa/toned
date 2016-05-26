toned
==========

*toned* is a python package to allow parallelized recursive text file search with boolean operations
It is NOT a lexer as a lexical analyzer is much more complex.
*toned* applies a layer on top of search keywords to convert them into regular expressions.
This way, users who are not good with regex can search within files.
*toned* has been unit-tested with python 2.7.

How to install:
`pip install toned`


**Examples:**
```
from toned import finder
DATA_DIR = '/tmp'
keywords = '(word1 or word2) and not word3'
print finder.find_in_dir(keywords,\
	DATA_DIR, multiline=True,\
        name_pattern='*.txt')
```
Output:
```
{'/tmp/sample1.txt': ['this is word1', 'this is word2'],
 '/tmp/sample2.txt': ['word1 followed by word2']}
```

If you want to specify the file:
```
from toned import finder
keywords = '(word1 or word2) and not word3'
files = ['/tmp/sample1.txt', '/tmp/sample2.txt']
print finder.find_in_files(keywords,\
	files, ignore_case=True)
```

A useful trick is that you can use a dot to find any character.
For example, you want to seach for either 'red box' or 'red-box'.
That can be searched like so:
```
keywords = 'red.box'
print finder.find_in_dir(keywords)
```

Limitations:
Some punctuations are not escaped and therefore after converting to regex puntuations might be problematic.
Please report issues on github to be addressed.
You cannot use this package for seaching through pdf files.
The fastest pythonic way to search through pdf files is to first convert them into text files using PdfMiner and then use this package to  search through them.

**Main method signatures:**
```
def find_in_files(keyword, files, multiline=False,\
                  ignore_case=True, worker_count=WORKER_COUNT):
    """
    @keyword: string
    @files: list of string text file paths
    @ignore_case: boolean
    @multiline: boolean
    @worker_count: int - the number of processes used for parallel searching
    returns a dict where the keys are the path of the files that matched
        and each value is a list of strings (matched sentences)
    """
```

```
def find_in_dir(keyword, root_dir, multiline=False,\
                ignore_case=True, worker_count=WORKER_COUNT,\
                name_pattern='*'):
    """
    @keyword: string
    @root_dir: the directory to start the recursive search from
    @name_pattern: string pattern for matching the filenames
        default is '*' which means any file
    @ignore_case: boolean
    @multiline: boolean
    @worker_count: int- the number of processes used for parallel searching
    returns a dict where the keys are the path of the files that matched
        and each value is a list of strings (matched sentences)
    """
```

Lastly, please feel free to report bugs or ask for features.
