#!/usr/bin/env python3

from pprint import pprint
from dictd import Dictd

x = Dictd.lookup("shovel")

pprint(x)


x = Dictd.parts_of_speech("shovel")

pprint(x)
