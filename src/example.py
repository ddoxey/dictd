#!/usr/bin/env python3

import os
import sys
from pprint import pprint

sys.path.append(os.path.dirname(__file__))

from dictd import Dictd

x = Dictd.lookup("shovel")

pprint(x)