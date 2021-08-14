# Dictd

This is wrapper for the dict Linux command line program, which distributes as the
"dictd" package on RedHat and Debian systems.

The objective of this module is to bring all of data in the Dict.org database to
life in Python with a consistent data structure. This is somewhat of a challenge,
given the considerable variation in the Dict.org free form human readable text.


# Usage

```
    from dictd import Dictd

    definitions = Dictd.lookup("shovel")
```

The definitions dict looks like:

```
    { [source name]: [
        { 'source': [source name tokens],
          'entries': [
            { 'pos': [parts of speech],
              'definition': [text of definition]},
            { 'pos': [parts of speech],
              'definition': [text of definition]},
            ...
```

A given source may appear multiple times, and each source entry may have multiple
definitions, or a list of synonyms.


# See Also

This module is unrelated to PyDictionary which might serve your needs.
