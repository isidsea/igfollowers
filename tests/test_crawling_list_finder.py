import os
import sys

TEST_DIR   = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.join(TEST_DIR, '..')
sys.path.insert(0, PARENT_DIR)

from lib.factory.finder import FinderFactory
from lib.exceptions     import CannotFindAccount
import pytest

def test_find():
	finder = FinderFactory.get_finder(FinderFactory.CRAWLING_LIST)
	result = finder.find("toyotaid")
	del result["_id"]

	correct_result = {
	    "displayName": "Toyota Indonesia",
	    "modelName": "",
	    "brandName": "Toyota",
	    "url": "https://www.instagram.com/hyundaiph/",
	    "userName": "toyotaid",
	    "country": "IDN",
	    "is_active": True
	}
	assert result == correct_result

def test_find_not_active():
	with pytest.raises(Exception):
		finder = FinderFactory.get_finder(FinderFactory.CRAWLING_LIST)
		result = finder.find("hyundaiph")