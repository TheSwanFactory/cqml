#!/usr/bin/env python3
import pytest
from .context import cqml, TEST_YAML
from .db_mock import spark

def test_root():
    root = cqml.root("pipes")
    assert root
    #assert "cqml" in keys
