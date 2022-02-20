#!/usr/bin/env python3

import sys
sys.path.insert(0,'..')

import pytest
from cqml import from_file,upgrade_file
TEST_YAML="pipes/cqml_test.yml"

def test_from_file():
        cvm = from_file(TEST_YAML, None)
        assert(cvm)
        assert(cvm.yaml)
