#!/usr/bin/env python3
import pytest
from .context import cqml, TEST_YAML
from .db_mock import spark

T_KEY="test/cqml"

@pytest.fixture
def root():
    root = cqml.root("pipes")
    return root

def test_root(root):
    assert root

def test_keys(root):
    keys = root.keys()
    assert keys
    assert keys[0]
    assert T_KEY in keys

def test_new(root):
    cvm = root.new(spark, T_KEY)
    assert cvm
    assert "test" == cvm.log("test")
