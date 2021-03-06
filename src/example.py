#!/usr/bin/env python3

import sys
from pprint import pprint
from dictd import Dictd


def run(word):

    print('Definitions:')
    x = Dictd.lookup(word)
    pprint(x)

    print("")

    print('Parts of Speech:', end=" ")
    x = Dictd.parts_of_speech(word)
    pprint(x)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('USAGE: {sys.argv[0]} <word>', file=sys.stderr)
    else:
        run(sys.argv[1])
