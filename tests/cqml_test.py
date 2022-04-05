#!/usr/bin/env python3
import pytest
from .context import cqml, TEST_YAML, DDIR
from .db_mock import spark

@pytest.fixture
def cvm():
    cvm = cqml.from_file(TEST_YAML, spark)
    cvm.test_id(DDIR)
    return cvm

def get_action(cvm, key):
    cvm.test_id(key)
    for a in cvm.cactions:
        if a['id'] == key: return a
    return None

def test_load(cvm):
    assert cvm.df["test1"]

def test_select(cvm):
    it = cvm.test_id("selected")
    #cvm.df["selected"]
    assert it
    assert it.num
    assert 'num' in it.columns
    #assert 'sku' in it.columns # alias
    # how to test filter with Mock?

def test_merge(cvm):
    dev = cvm.test_id("merged")
    assert dev
    assert 'num' in dev.columns # alias
    assert 'note' not in dev.columns # alias

def test_call(cvm):
    a = get_action(cvm, "count_days")
    assert a['sql'] == 'datediff(current_date(),dat)'

def test_coalesce(cvm):
    a = get_action(cvm, "call_coalesce")
    assert a['sql'] == "coalesce(text,'Unassigned')"

def test_space(cvm):
    a = get_action(cvm, "concat_space")
    assert a['sql'] == "num||' '||letter"
