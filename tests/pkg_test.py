#!/usr/bin/env python3
import pytest
from .context import cqml, TEST_KEY
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

#def test_all(): dict = cqml.pkg_all(spark, 'tests')
    #assert 'cqml_test' in dict
