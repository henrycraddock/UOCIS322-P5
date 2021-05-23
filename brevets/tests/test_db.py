"""
Nose tests for MongoDB database usage
"""

import os
from pymongo import MongoClient
import nose
import logging

logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)

client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.testdb

# Test entries
entry_1 = {
    'km': 150.0,
    'open': '2021-01-02T04:25',
    'close': '2021-01-02T10:00'
}

entry_2 = {
    'miles': 127.381055,
    'km': 205.0,
    'open': '2021-01-02T05:53',
    'close': '2021-01-02T01:20'
}

entry_3 = {
    'miles': 93.205650,
    'km': 150.0,
    'open': '2021-01-02T04:25',
    'close': '2021-01-02T10:00'
}


def test_single_insert():
    """Test a single insert to the database"""
    db.testdb.insert_one(entry_1)
    assert db.testdb.find_one({'km': 150.0}) == entry_1
    db.testdb.delete_one(entry_1)
    assert db.testdb.find_one({'km': 150.0}) is None


def test_multiple_entries():
    """Test db functionality with multiple inserts, deletions, and checks"""
    db.testdb.insert_one(entry_1)
    db.testdb.insert_one(entry_2)
    assert db.testdb.find_one({'km': 150.0}) == entry_1
    db.testdb.insert_one(entry_3)
    assert db.testdb.find_one({'open': '2021-01-02T05:53'}) == entry_2
    assert db.testdb.find_one({'km': 150.0, 'miles': 93.205650}) == entry_3
    db.testdb.delete_one(entry_1)
    db.testdb.delete_one(entry_2)
    assert db.testdb.find_one({'open': '2021-01-02T05:53'}) is None
    assert db.testdb.find_one({'km': 150.0}) == entry_3
    db.testdb.delete_one(entry_3)
    assert db.testdb.find_one({'km': 150.0}) is None
