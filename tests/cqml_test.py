#!/usr/bin/env python3
import pytest
from .context import cqml, TEST_YAML, DDIR
from .db_mock import spark

@pytest.fixture
def cvm():
    cvm = cqml.from_file(TEST_YAML, spark)
    cvm.test_id(DDIR)
    return cvm

def test_load(cvm):
    assert cvm.df["test1"]

def test_select(cvm):
    cvm.test_id("selected")
    it = cvm.df["selected"]
    assert it
    assert it.num
    assert 'num' in it.columns
    #assert 'sku' in it.columns # alias
    # how to test filter with Mock?

def test_merge(cvm):
    cvm.test_id("merged")
    dev = cvm.df["merged"]
    assert dev
    assert 'next' in dev.columns # alias
    assert 'note' not in dev.columns # alias

def test_call(cvm):
    cvm.test_id("count_days")
    for a in cvm.cactions:
        if a['id'] == 'count_days':
            assert a['sql'] == 'datediff(current_date(),dat)'
