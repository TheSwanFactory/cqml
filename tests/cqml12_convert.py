#!/usr/bin/env python3

import sys
sys.path.insert(0,'..')

from cqml import upgrade_file

if len(sys.argv) > 1:
    files = sys.argv[1:]
    for file in files:
        print(file)
        upgrade_file(file)
