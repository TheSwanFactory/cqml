#!/usr/bin/env python3
import pytest
from .context import cqml
from .db_mock import spark
TEST_YAML="tests/pipes/cqml_test.yml"

@pytest.fixture
def df():
    cvm = cqml.make_frames(TEST_YAML, spark)
    return cvm.df

def test_load(df):
    assert df["items"]

def test_select(df):
    it = df["items"]
    assert it
    assert it.item_id
    assert 'item_id' in it.columns
    assert 'sku' in it.columns # alias
    # how to test filter with Mock?

def test_merge(df):
    dev = df["na_devices"]
    assert dev
    assert 'sku' in dev.columns # alias
    assert 'item_id' not in dev.columns # alias
