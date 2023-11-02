import pytest
import requests
import sys
from os.path import abspath, dirname

# Add the path to the project root directory
sys.path.insert(0, abspath(dirname(__file__) + "/.."))

# Import app from root directory

from app import app


def test_root_page():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b'<html lang="en" op="news">' in response.data