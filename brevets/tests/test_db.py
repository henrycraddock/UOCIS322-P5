"""
Nose tests for MongoDB database usage
"""

import sys
import os

curr_dir = os.path.dirname(__file__)
flask_dir = os.path.join(curr_dir, '..')
sys.path.append(flask_dir)

from flask_brevets import db_insert, db_find_one, db_delete_one
import nose
import logging

logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)


# Test entries
entry_1 = {'num': '1', 'data[0][index]': '0', 'data[0][miles]': '37.282260',
           'data[0][km]': '60', 'data[0][location]': '', 'data[0][open]': '2021-01-01T01:46',
           'data[0][close]': '2021-01-01T04:00'}

entry_2 = {'num': '3', 'data[0][index]': '0', 'data[0][miles]': '49.709680',
            'data[0][km]': '80', 'data[0][location]': '', 'data[0][open]': '2021-01-01T02:21',
            'data[0][close]': '2021-01-01T05:20', 'data[1][index]': '1',
            'data[1][miles]': '74.564520', 'data[1][km]': '120', 'data[1][location]': '',
            'data[1][open]': '2021-01-01T03:32', 'data[1][close]': '2021-01-01T08:00',
            'data[2][index]': '2', 'data[2][miles]': '124.274200', 'data[2][km]': '200',
            'data[2][location]': '', 'data[2][open]': '2021-01-01T05:53',
            'data[2][close]': '2021-01-01T13:30'}


def test_single_insert():
    """Test a single insert to the database"""
    db_insert(entry_1)
    assert db_find_one({'km': 60.0}) is not None
    assert db_find_one({'km': 50.0}) is None
    db_delete_one({'km': 60.0})
    assert db_find_one({'km': 60.0}) is None


def test_multiple_entries():
    """Test db functionality with multiple insertions, deletions, and checks"""
    db_insert(entry_1)
    assert db_find_one({'km': 60.0}) is not None
    assert db_find_one({'km': 80.0}) is None
    db_insert(entry_2)
    assert db_find_one({'km': 80.0}) is not None
    assert db_find_one({'km': 200.0}) is not None
    db_delete_one({'miles': 74.564520})
    assert db_find_one({'miles': 74.564520}) is None
    db_delete_one({'open': '2021-01-01T01:46'})
    db_delete_one({'km': 80.0})
    db_delete_one({'close': '2021-01-01T13:30'})
    assert db_find_one({'km': 200.0}) is None
    assert db_find_one({'km': 80.0}) is None
    assert db_find_one({'km': 60.0}) is None
