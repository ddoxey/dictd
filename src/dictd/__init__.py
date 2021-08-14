import subprocess
from pprint import pprint, pformat
from collections import defaultdict
import re


class Dictd:

    class Entry:
        p_of_s = None
        tokens = None

        def __init__(self):
            self.p_of_s = []
            self.tokens = []
            return

        def add(self, token):
            self.tokens.append(token)

        def last(self):
            if len(self.tokens) == 0:
                return None
            return self.tokens[-1]

        def pop(self):
            if len(self.tokens) == 0:
                return
            self.tokens.pop()

        def pos(self, pos=None):
            if pos is not None and pos not in self.p_of_s:
                self.p_of_s.append(pos)
            return len(self.p_of_s)

        def size(self):
            return len(self.tokens)

        def definition(self):
            return {
                'pos': self.p_of_s,
                'definition': ' '.join(self.tokens)}

        def flush(self):
            d = self.definition()
            self.p_of_s = []
            self.tokens = []
            return d

        def __repr__(self):
            return pformat(self.definition())


    DICT = '/usr/bin/dict'

    KnownPOS = {
        'n': 'n',
        'adj': 'adj',
        'v': 'v',
        'pro': 'pro',
        'adv': 'adv',
        'prep': 'prep',
        'conj': 'conj',
        'int': 'int',
        'pron': 'pron',
    }


    @classmethod
    def _get_pos_(cls, candidate):
        candidate = candidate.lower().strip().strip('.')
        if candidate in cls.KnownPOS:
            return cls.KnownPOS[candidate]
        return None


    @classmethod
    def _tokenize(cls, line, sep=""):
        separator = re.compile(sep + r'\s+')
        return [t.strip() for t in re.split(separator, line)]


    @classmethod
    def _split_mobythesaurus_entries_(cls, word, lines):
        synonyms = []

        for line in [l.strip() for l in lines]:

            if len(line) == 0:
                continue

            if len(synonyms) == 0 and re.search(r'^[0-9]+[ ]Moby', line):
                continue

            tokens = Dictd._tokenize(line, sep=',')

            for token in [t.strip().strip(',') for t in tokens]:

                if len(token) > 0:
                    synonyms.append(token)

        return [{'synonyms': synonyms}]


    @classmethod
    def _split_gcide_entries_(cls, word, lines):
        entries = []
        entry = Dictd.Entry()
        bracket_depth = 0
        last_pos = None

        while entry.pos() == 0 or bracket_depth > 0:

            tokens = Dictd._tokenize(lines.pop(0))

            for token in [t for t in tokens if len(t) > 0]:
                pos = None
                if bracket_depth == 0:
                    pos = Dictd._get_pos_(token)
                if pos is not None:
                    entry.pos(pos)
                    last_pos = pos
                else:
                    bracket_depth += token.count('[')
                    bracket_depth -= token.count(']')

        for line in [l.strip() for l in lines]:

            if len(line) == 0:
                continue

            if re.search(r'^\s*[[][0-9]+[ ]Webster[]]$', line):
                entry.add(line)
                entries.append(entry.flush())
                entry.pos(last_pos)
                continue

            tokens = [t for t in Dictd._tokenize(line) if len(t) > 0]

            if tokens[0].startswith('{') and tokens[0].endswith('}'):
                entry.flush()
                break

            for n, token in enumerate(tokens):
                if n == 0 and re.search(r'^[0-9]+[:.]$', token):
                    if entry.size() > 0:
                        entries.append(entry.flush())
                        entry.pos(last_pos)
                else:
                    entry.add(token)

        if entry.size() > 0:
            entries.append(entry.flush())

        return entries


    @classmethod
    def _split_wn_entries_(cls, word, lines):
        entries = []
        entry = Dictd.Entry()
        last_pos = None

        for line in [l.strip() for l in lines]:

            if len(line) == 0:
                continue

            if line.lower() == word.lower():
                continue

            tokens = Dictd._tokenize(line)

            for n, token in enumerate([t for t in tokens if len(t) > 0]):

                if n == 0:
                    pos = cls._get_pos_(token)
                    if pos is not None:
                        if entry.pos() > 0:
                            entries.append(entry.flush())
                        entry.pos(pos)
                        last_pos = pos
                        continue

                if n <= 1 and re.search(r'^[0-9]+[:.]$', token):

                    if entry.pos() == 0 and last_pos is not None:
                        entry.pos(last_pos)

                    if entry.size() > 0:
                        entries.append(entry.flush())

                    continue

                if entry.pos() == 0:
                    entry.pos(last_pos)

                entry.add(token)

        if entry.size() > 0:
            entries.append(entry.flush())

        return entries


    @classmethod
    def _split_definition_entries_(cls, word, source, lines):

        parse_for = {
            'wn': cls._split_wn_entries_,
            'gcide': cls._split_gcide_entries_,
            'moby-thesaurus': cls._split_mobythesaurus_entries_,
        }

        source_abbr = source.split('\t')

        if len(source_abbr) < 3 or source_abbr[2] not in parse_for:
            return None

        return parse_for[source_abbr[2]](word, lines)


    @classmethod
    def _fetch_dictd_result_(cls, word):
        cmd = [cls.DICT, '-f', word]
        app = subprocess.Popen(cmd, stdout = subprocess.PIPE)
        for bline in app.stdout:
            yield bline.decode('utf8')


    @classmethod
    def _parse_(cls, word, lines):

        definition_for = {}
        definition = { 'lines': [] }

        def _ingest(definition):
            if len(definition['lines']) == 0:
                return
            definition['entries'] = cls._split_definition_entries_(
                word.title(),
                definition['source'],
                definition['lines'])
            if definition['entries'] is not None:
                source = '0.{}'.format(definition['source'].replace('\t', " "))
                while source in definition_for:
                    n, src = source.split('.', 1)
                    source = '{}.{}'.format(int(n) + 1, src)
                del definition['lines']
                definition['source'] = definition['source'].split('\t')
                definition_for[source] = definition

        for line in lines:

            if line[0] != ' ':

                _ingest(definition)

                definition = {
                    'source': line.strip(),
                    'lines': [],
                }

            elif 'source' in definition:

                definition['lines'].append(line)

        _ingest(definition)

        return definition_for


    @classmethod
    def lookup(cls, word):

        raw_text_lines = cls._fetch_dictd_result_(word)

        definition_for = cls._parse_(word, raw_text_lines)

        if len(definition_for) == 0:
            return None

        sources = list(definition_for.keys())

        for source in sources:
            if len(definition_for[source]['entries']) == 0:
                del definition_for[source]

        return definition_for


    @classmethod
    def parts_of_speech(cls, word):

        definition_for = cls.lookup(word)

        if definition_for is None:
            return None

        parts_of_speech = defaultdict(int)

        for source in definition_for:
            for entry in definition_for[source]['entries']:
                if 'pos' in entry:
                    for pos in entry['pos']:
                        parts_of_speech[pos] += 1

        if len(parts_of_speech) == 0:
            return None

        return dict(parts_of_speech)
