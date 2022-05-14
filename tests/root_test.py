#!/usr/bin/env python3
import pytest
from .context import cqml, TEST_YAML
from .db_mock import spark

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
    assert "test/cqml" in keys
