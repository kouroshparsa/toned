"""
    This module has the unittests
    :copyright: (c) 2016 by Kourosh Parsa.
"""
from toned import finder
import re
import yaml
import os
from glob import glob
from nose.tools import assert_raises
from nose_parameterized import parameterized
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DATA = yaml.load(open("%s/data.yaml" % BASE_DIR, "r"))
DATA_DIR = os.path.join(BASE_DIR, 'data')

@parameterized([(val['val'], val['start'], val['end'])
                for val in TEST_DATA['close_ind']])
def test_close_ind(val, start_ind, end_ind):
    assert finder.get_close_ind(val, start_ind) == end_ind


@parameterized([(val['keyword'], val['sentence'], val['match'])
                for val in TEST_DATA['regex_test']])
def test_regex(keyword, sentence, is_matched):
    pattern = finder.get_regex(keyword)
    if is_matched:
        assert re.match(pattern, sentence), 'pattern: %s' % pattern
    else:
        assert re.match(pattern, sentence) == None, 'pattern: %s' % pattern


def test_invalid_regex():
    """ validate proper exception thrown """
    files = glob('%s/*' % DATA_DIR)
    assert_raises(re.error, finder.find_in_files, '[\\[', files)

def test_basic_find():
    """ validates single line match in a directory """
    res = finder.find_in_dir('small-cell', DATA_DIR, name_pattern='*.txt')
    assert res is not None, 'Did not find any match!'
    filenames = sorted([os.path.basename(path) for path in res.keys()])
    assert filenames == ['sample1.txt', 'sample2.txt']

def test_complex_find():
    """ validates multiline match """
    res = finder.find_in_dir('small-cell and not non.small-cell',\
                             DATA_DIR, name_pattern='*.txt')
    assert res is not None, 'Did not find any match!'
    filenames = sorted([os.path.basename(path) for path in res.keys()])
    assert filenames == ['sample1.txt']
    assert res.values()[0] == ['criteria: small-cell'], 'Found: %s' % res.values()

    res = finder.find_in_dir('small-cell and 2012',\
                             DATA_DIR, multiline=True,\
                             name_pattern='*.txt')

    filenames = [os.path.basename(path) for path in res.keys()]
    assert filenames == ['sample1.txt']
    
