#!/usr/bin/env python3
import pytest
from .context import cqml, TEST_YAML
from .db_mock import spark

def test_yml_keys():
    keys = cqml.yml_keys("pipes/test")
    assert keys
    assert "cqml" in keys

def test_yml_tree():
    keys = cqml.yml_tree("pipes")
    assert keys
    assert len(keys) == 2
