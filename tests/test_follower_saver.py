import os
import sys

TEST_DIR   = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.join(TEST_DIR, '..')
sys.path.insert(0, PARENT_DIR)

from lib.factory.saver import SaverFactory
import pymongo
import pytest
import re

@pytest.fixture
def account():
	return {
		"userName": "test",
		"displayName": "Test Display Name",
		"url": "htpp://example.com"
	}

@pytest.fixture
def follower():
	return {
		"username": "follower1",
		"display_name": "Follwer 1",
		"user_link": "http://example.com"
	}

def test_save(account, follower):
	saver 		  = SaverFactory.get_saver(SaverFactory.FOLLOWER)
	saver.account = account
	saver.save(follower)

	conn = pymongo.MongoClient("mongodb://mongo:27017/ig")
	db   = conn["ig"]

	docs = db.data.find({"$and":[
		{"username": re.compile(account["userName"], re.IGNORECASE)},
		{"followers.username": re.compile(follower["username"], re.IGNORECASE)}
	]})
	conn.close()
	assert docs.count() == 1

def test_delete(account):
	conn = pymongo.MongoClient("mongodb://mongo:27017/ig")
	db   = conn["ig"]

	db.data.delete_many({"username": re.compile(account["userName"], re.IGNORECASE)})
	docs = db.data.find({"username": re.compile(account["userName"], re.IGNORECASE)})

	conn.close()
	assert docs.count() == 0