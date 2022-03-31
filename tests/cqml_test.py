#!/usr/bin/env python3
import pytest
from .context import cqml, TEST_YAML
from .db_mock import spark

@pytest.fixture
def cvm():
    cvm = cqml.make_frames(TEST_YAML, spark, True)
    return cvm

def test_load(cvm):
    assert cvm.df["test1"]

def test_select(cvm):
    it = cvm.df["selected"]
    assert it
    assert it.num
    assert 'num' in it.columns
    #assert 'sku' in it.columns # alias
    # how to test filter with Mock?

def test_merge(cvm):
    dev = cvm.df["merged"]
    assert dev
    assert 'num' in dev.columns # alias
    assert 'note' not in dev.columns # alias

def test_call(cvm):
    for a in cvm.cactions:
        if a['id'] == 'days_unseen':
            assert a['sql'] == 'datediff(current_date(),_fivetran_synced)'
