#!/usr/bin/env python3
import pytest
from .context import cqml, TEST_YAML
from .db_mock import spark

def test_root():
    root = cqml.root("pipes")
    assert root
    keys = root.keys()
    assert keys
    assert "test/cqml" in keys
