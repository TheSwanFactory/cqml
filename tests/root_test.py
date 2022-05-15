#!/usr/bin/env python3
import pytest
from .context import cqml, TEST_KEY
from .db_mock import spark

@pytest.fixture
def root():
    root = cqml.Root("pipes")
    return root

def test_root(root):
    assert root

def test_keys(root):
    keys = root.keys()
    assert keys
    assert keys[0]
    assert TEST_KEY in keys

def test_new(root):
    cvm = root.new(spark, TEST_KEY)
    assert cvm
    assert "test" == cvm.log("test")
