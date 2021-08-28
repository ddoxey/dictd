# Dictd

This is wrapper for the dict Linux command line program, which distributes as the
"dictd" package on RedHat and Debian systems.

The objective of this module is to bring all of data in the Dict.org database to
life in Python with a consistent data structure. This is somewhat of a challenge,
given that depends on parsing the free form human readable text from Dict.org.

Currently this is known to do a good job of parsing 'wn', 'gcide', and the
'moby-thesaurus' definitions.


# Usage

```
    from dictd import Dictd

    definitions = Dictd.lookup("shovel")
```

The definitions dict looks like:

```
    { [source-keyword]: [
        { 'source': [source name],
          'entries': [
            { 'pos': [parts of speech],
              'definition': [text of definition]},
            { 'pos': [parts of speech],
              'definition': [text of definition]},
            ...
```

If you only care about the part of speech:

```
    Dictd.parts_of_speech("shovel")
```

Which returns a dict of each POS with the number of times it appears in the
definitions.

```
    {'n': 5, 'v': 3}
```


A given source may appear multiple times, and each source entry may have multiple
definitions, or a list of synonyms.


# See Also

This module is unrelated to PyDictionary which might serve your needs.
