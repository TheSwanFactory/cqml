#!/usr/bin/env python3
import pytest
from .context import *
from .db_mock import spark

@pytest.fixture
def root():
    root = cqml.Root("pipes")
    return root

def test_pkg(root):
    dict = root.pkg(spark, TEST_KEY, True)
    assert 'pkg' in dict
    assert 'html' in dict
    assert 'actions' in dict

def test_pkg_demo(root):
    dict = root.pkg(spark, TEST_DEMO, True)
    assert 'pkg' in dict
    assert 'html' in dict
    assert 'actions' in dict

def test_box(root):
    cvm = root.new(spark, TEST_KEY)
    cvm.test_id(DDIR)
    it = cvm.test_id("box_details")
    assert it

def test_all(root):
    dict = root.pkg(spark, 'pipes/all', True)
    assert 'all' in dict
