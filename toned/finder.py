"""
    This module searches through files
    :copyright: (c) 2016 by Kourosh Parsa.
"""
import re
from multiprocessing import Pool
import subprocess
import os
import re
import traceback
WORKER_COUNT = 20

def get_close_ind(val, ind):
    """
    @val: string
    @ind: int - index of '(' in val
    """
    ops = 1
    ind += 1
    while ind < len(val):
        char = val[ind]
        if char == '(':
            ops += 1
        elif char == ')':
            ops -= 1
            if ops == 0:
                return ind
        ind += 1
    return -1


def __get_and_regex(val1, val2):
    """
    @val1, @val2: str
    returns a regex string
    """
    val1 = __get_regex(val1)
    if ')(' in val1 or ')|(' in val1:
        val1 = '(%s)' % val1

    val2 = __get_regex(val2)
    if ')(' in val2 or ')|(' in val2:
        val2 = '(%s)' % val2
    return '{}{}'.format(val1, val2)

def __get_or_regex(val1, val2):
    """
    @val1, @val2: str
    returns a regex string
    """
    val1 = __get_regex(val1)
    val2 = __get_regex(val2)
    return '{}|{}'.format(val1, val2)

def __get_regex(val):
    """
    @val: string
    returns a regex string
    """
    #import pdb;pdb.set_trace()
    for ind, char in enumerate(val):
        if char == '(':
            closeind = get_close_ind(val, ind)
            if closeind == len(val) - 1:
                return __get_regex(val[1:-1])

            next_val = val[closeind+1:].strip().lower()
            if next_val.startswith('and '):
                return __get_and_regex(val[0: closeind+1], val[closeind+1:])

            elif next_val.startswith('or '):
                return __get_or_regex(val[0: closeind+1], val[closeind+1:])

        elif val[ind+1:].lower().startswith(' and '):
            return __get_and_regex(val[0:ind+1], val[ind+6:])

        elif val[ind+1:].lower().startswith(' or '):
            return __get_or_regex(val[0:ind+1], val[ind+5:])

    if val.lower().startswith('not '):
        return r'(?!.*\b{}\b)'.format(val[4:])
    return r'(?=.*\b{}\b)'.format(val)


def get_regex(keyword):
    """
    @keyword: string
    returns a regex string pattern
    """
    keyword = re.sub(r' +', ' ', keyword) # remove redundant spaces
    # escape some characters:
    keyword = re.sub(r'\[', '\\[', keyword)
    keyword = re.sub(r'\]', '\\]', keyword)
    keyword = re.sub(r'\{', '\\{', keyword)
    keyword = re.sub(r'\}', '\\}', keyword)
    keyword = re.sub(r'\*', '\\*', keyword)
    keyword = re.sub(r'\=', '\\=', keyword)
    keyword = re.sub(r'\-', '\\-', keyword)
    keyword = re.sub(r'\+', '\\+', keyword)
    keyword = re.sub(r'\?', '\\?', keyword)
    keyword = re.sub(r'\$', '\\$', keyword)
    keyword = re.sub(r'\$', '\\$', keyword)
    return __get_regex(keyword)


def find_in_file_per_line(path, regex, ignore_case):
    """
    @path: string, file path
    @regex: regex pattern to match per line in the file
    @ignore_case: boolean
    returns either None or a tuple (path, list of matched lines)
    """
    matched_lines = []
    for line in open(path, 'r'):
        line = line.strip()
        params = [regex, line]
        if ignore_case:
            params.append(re.IGNORECASE)
        if re.match(*params) is not None:
            matched_lines.append(line)

    if len(matched_lines) > 0:
        return (path, matched_lines)
    return None


def find_in_file_multiline(path, regex, ignore_case):
    """
    @path: string, file path
    @regex: regex pattern to match per line in the file
    @ignore_case: boolean
    returns either None or a tuple (path, list of matched lines)
    """
    content = open(path, 'r').read()
    params = [regex, content, re.MULTILINE|re.DOTALL]
    if ignore_case:
        params = [regex, content, re.IGNORECASE|re.MULTILINE|re.DOTALL]

    if re.match(*params) is not None:
        res = find_in_file_per_line(path, regex, ignore_case)
        matched_lines = []
        if res is not None:
            matched_lines = res[1]
        return (path, matched_lines)
    return None


def find_in_file(path, regex, multiline=False, ignore_case=True):
    """
    @path: string, file path
    @regex: regex pattern to match per line in the file
    @ignore_case: boolean
    @multiline: boolean
    returns either None or a tuple (path, list of matched lines)
    """
    if multiline:
        return find_in_file_multiline(path, regex, ignore_case)
    return find_in_file_per_line(path, regex, ignore_case)


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
    regex = get_regex(keyword)
    try:
        re.compile(regex) # validate it
    except re.error:
        raise re.error('Invalid regex. Make sure your keywords do not have punctuations.')

    results = {}
    pool = Pool(worker_count)
    pool.daemon = True
    workers = []
    for path in files:
        workers.append(pool.apply_async(find_in_file,\
            (path, regex, multiline, ignore_case)\
                                        ))
    for worker in workers:
        res = worker.get()
        if res is not None:
            path, val = res
            results[path] = val
    pool.terminate()
    return results


def find_in_dir(keyword, root_dir, multiline=False,\
                ignore_case=True, worker_count=WORKER_COUNT,\
                name_pattern='.*'):
    """
    @keyword: string
    @root_dir: the directory to start the recursive search from
    @name_pattern: regex pattern for matching the filenames
        default is '.*' which means any file
    @ignore_case: boolean
    @multiline: boolean
    @worker_count: int- the number of processes used for parallel searching
    returns a dict where the keys are the path of the files that matched
        and each value is a list of strings (matched sentences)
    """
    file_paths = []
    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            if re.match(name_pattern, filename):
                file_paths.append(os.path.join(root, filename))

    file_paths = file_paths
    return find_in_files(keyword, file_paths,\
                         ignore_case=ignore_case,\
                         multiline=multiline,\
                         worker_count=worker_count)

