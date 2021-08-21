import unittest
from dictd import Dictd


class TestDictionaryParsers(unittest.TestCase):

    def test_foldoc_ca_n(self):
        word = 'ca'
        foldoc = '''
  CA

     1. <theory, architecture> {cellular automaton}.

     2. <company> {Computer Associates}.

     3. <cryptography> {Certificate Authority}.
'''
        result = Dictd._split_foldoc_entries_(word, foldoc.split('\n'))

        expect = [
            {'definition': 'Cellular Automaton (Theory, Architecture)'},
            {'definition': 'Computer Associates (Company)'},
            {'definition': 'Certificate Authority (Cryptography)'},
        ]

        self.assertEqual(result, expect, f'Correct parse of FOLDOC "{word}"')


    def test_vera_ca_n(self):
        word = 'ca'
        vera = '''
  CA
           Certification Authority (cryptography, PKI)

'''
        result = Dictd._split_vera_entries_(word, vera.split('\n'))

        expect = [
            {'definition': 'Certification Authority (cryptography, PKI)'}
        ]

        self.assertEqual(result, expect, f'Correct parse of VERA "{word}"')


    def test_gcide_ca_n(self):
        word = 'ca'
        gcide = '''
  Ca \Ca\ n.
     the chemical symbol for calcium, the fifth most abundant
     element in the earth's crust, having an atomic number of 20.

     Syn: calcium.
          [WordNet 1.5]
'''
        result = Dictd._split_gcide_entries_(word, gcide.split('\n'))

        expect = [
            {'definition': 'The chemical symbol for calcium, the fifth most abundant '
                           'element in the earth\'s crust, having an atomic number of 20. '
                           'Syn: calcium. [WordNet 1.5]',
             'pos': ['n']}
        ]

        self.assertEqual(result, expect, f'Correct parse of GCIDE "{word}"')


    def test_gcide_ca_adv_prep(self):
        word = 'ca'
        gcide = '''
  circa \cir"ca\ (s[~e]r"k[.a]), adv., prep. [L.]
     Approximately; about; commonly abbreviated {ca.}; -- used
     especially before dates and numerical measures; as, he was
     born circa 1650; ca. 50 feet high.

     Syn: ca.
          [PJC]
'''
        result = Dictd._split_gcide_entries_(word, gcide.split('\n'))

        expect = [
            {'definition': 'Approximately; about; commonly abbreviated {ca.}; -- used '
                           'especially before dates and numerical measures; as, he was '
                           'born circa 1650; ca. 50 feet high. Syn: ca. [PJC]',
             'pos': ['adv', 'prep']}
        ]

        self.assertEqual(result, expect, f'Correct parse of GCIDE "{word}"')


    def test_gcide_shovel_v(self):
        word = 'shovel'
        gcide = '''
  Shovel \Shov"el\, v. t. [imp. & p. p. {Shoveled}or {Shovelled};
     p. pr. & vb. n. {Shoveling} or {Shovelling}.]
     1. To take up and throw with a shovel; as, to shovel earth
        into a heap, or into a cart, or out of a pit.
        [1913 Webster]

     2. To gather up as with a shovel.
        [1913 Webster]
'''
        result = Dictd._split_gcide_entries_(word, gcide.split('\n'))

        expect = [
            {'definition': 'To take up and throw with a shovel; as, to shovel earth '
                           'into a heap, or into a cart, or out of a pit. [1913 Webster]',
             'pos': ['v']},
            {'definition': 'To gather up as with a shovel. [1913 Webster]',
             'pos': ['v']},
        ]

        self.assertEqual(result, expect, f'Correct parse of GCIDE "{word}"')


    def test_gcide_shovel_n(self):
        word = 'shovel'
        gcide = '''
  Shovel \Shov"el\, n. [OE. shovele, schovele, AS. scoft, sceoft;
     akin to D. schoffel, G. schaufel, OHG. sc?vala, Dan. skovl,
     Sw. skofvel, skyffel, and to E. shove. [root]160. See
     {Shove}, v. t.]
     An implement consisting of a broad scoop, or more or less
     hollow blade, with a handle, used for lifting and throwing
     earth, coal, grain, or other loose substances.
     [1913 Webster]

     {Shovel hat}, a broad-brimmed hat, turned up at the sides,
        and projecting in front like a shovel, -- worn by some
        clergy of the English Church. [Colloq.]

     {Shovelspur} (Zool.), a flat, horny process on the tarsus of
        some toads, -- used in burrowing.

     {Steam shovel}, a machine with a scoop or scoops, operated by
        a steam engine, for excavating earth, as in making railway
        cuttings.
        [1913 Webster]
'''
        result = Dictd._split_gcide_entries_(word, gcide.split('\n'))

        expect = [
            {'definition': 'An implement consisting of a broad scoop, or more or less '
                           'hollow blade, with a handle, used for lifting and throwing '
                           'earth, coal, grain, or other loose substances. '
                           '[1913 Webster]',
             'pos': ['n']},
        ]

        self.assertEqual(result, expect, f'Correct parse of GCIDE "{word}"')


    def test_wn_shovel(self):
        word = 'shovel'
        word_net = '''
  shovel
      n 1: a hand tool for lifting loose material; consists of a
           curved container or scoop and a handle
      2: the quantity a shovel can hold [syn: {shovel}, {shovelful},
         {spadeful}]
      3: a fire iron consisting of a small shovel used to scoop coals
         or ashes in a fireplace
      4: a machine for excavating [syn: {power shovel}, {excavator},
         {digger}, {shovel}]
      v 1: dig with or as if with a shovel; "shovel sand"; "he
           shovelled in the backyard all afternoon long"
'''
        result = Dictd._split_wn_entries_(word, word_net.split('\n'))

        expect = [
            {'definition': 'A hand tool for lifting loose material; consists of a '
                           'curved container or scoop and a handle',
             'pos': ['n']},
            {'definition': 'The quantity a shovel can hold [syn: {shovel}, '
                           '{shovelful}, {spadeful}]',
             'pos': ['n']},
            {'definition': 'A fire iron consisting of a small shovel used to scoop '
                           'coals or ashes in a fireplace',
             'pos': ['n']},
            {'definition': 'A machine for excavating [syn: {power shovel}, '
                           '{excavator}, {digger}, {shovel}]',
             'pos': ['n']},
            {'definition': 'Dig with or as if with a shovel; "shovel sand"; "he '
                           'shovelled in the backyard all afternoon long"',
             'pos': ['v']}]

        self.assertEqual(result, expect, f'Correct parse of WordNet "{word}"')


    def test_mobythesaurus_shovel(self):
        word = 'shovel'
        moby_thesaurus = '''
  59 Moby Thesaurus words for "shovel":
     backhoe, bail, bar spade, bore, bucket, burrow, coal shovel, cup,
     decant, delve, dig, dig out, dike, dip, dish, dish out, dish up,
     dredge, drill, drive, excavate, fork, furrow, garden spade, gouge,
     gouge out, groove, grub, gumming spade, ladle, lower, loy, mine,
     peat spade, posthole spade, pour, power shovel, quarry,
     salt shovel, sap, scoop, scoop out, scoop shovel, scrabble, scrape,
     scratch, scuff, shamble, sink, spade, split shovel, spoon, spud,
     steam shovel, stump spud, trench, trenching spade, trough,
     tunnel
'''

        result = Dictd._split_mobythesaurus_entries_(word, moby_thesaurus.split('\n'))

        expect = [
            {'synonyms': [
                'backhoe', 'bail', 'bar spade', 'bore', 'bucket', 'burrow', 'coal shovel', 'cup',
                'decant', 'delve', 'dig', 'dig out', 'dike', 'dip', 'dish', 'dish out', 'dish up',
                'dredge', 'drill', 'drive', 'excavate', 'fork', 'furrow', 'garden spade', 'gouge',
                'gouge out', 'groove', 'grub', 'gumming spade', 'ladle', 'lower', 'loy', 'mine',
                'peat spade', 'posthole spade', 'pour', 'power shovel', 'quarry',
                'salt shovel', 'sap', 'scoop', 'scoop out', 'scoop shovel', 'scrabble', 'scrape',
                'scratch', 'scuff', 'shamble', 'sink', 'spade', 'split shovel', 'spoon', 'spud',
                'steam shovel', 'stump spud', 'trench', 'trenching spade', 'trough',
                'tunnel']}]

        self.assertEqual(result, expect, f'Correct parse of Moby-Thesaurus "{word}"')


if __name__ == '__main__':
    unittest.main()
