#!/usr/bin/env python3
import pytest
from .context import cqml, TEST_YAML
from .db_mock import spark

def test_yml_keys():
    keys = cqml.yml_keys("pipes/test")
    assert keys
    assert "cqml" in keys

def test_yml_tree():
    rows = cqml.yml_tree("pipes")
    assert rows
    assert len(rows) == 2
    d0 = rows[0]
    assert "key" in d0
    
