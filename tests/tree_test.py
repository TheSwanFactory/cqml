#!/usr/bin/env python3
import pytest
from .context import cqml, TEST_YAML
from .db_mock import spark

def test_yml_keys():
    dict = cqml.yml_keys("pipes/test")
    assert dict
    assert "cqml" in dict

def skip_test_all():
    dict = cqml.pkg_all(spark, 'tests')
    assert 'cqml_test' in dict
