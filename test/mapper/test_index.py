import unittest

from contrib.pyas.src.pyas_v3 import As

from src.mappers.index import Index


class TestIndex(unittest.TestCase):

    def testSimple(self):

        index = {
            'table': 'tbl1',
            'parts': [
                ['_!#', Index.quote],
                ['col1', Index.quote, Index.cast, 'int'],
            ],
        }
        indexee = As(Index)(index)

        qExp = 'create index if not exists {} on tbl1 (_!#, cast(col1 as int))' \
            .format(indexee.name)
        qAct = As(Index)(index).createQuery(lambda c: c)
        self.assertEqual(qExp, qAct)

        def quote(c): return '|{}|'.format(c)
        qExp = 'create index if not exists {} on |tbl1| (|_!#|, cast(|col1| as int))'\
            .format(quote(indexee.name))
        qAct = As(Index)(index).createQuery(quote)
        self.assertEqual(qExp, qAct)

    def test_nested(self):
        index = {
            'table': 'ff<-l',
            'parts': [
                ['ff__id', Index.quote],
                [['__index', Index.quote], ' % 2'],
            ]
        }

        indexee = As(Index)(index)
        def quote(c): return '|{}|'.format(c)
        qExp = 'create index if not exists {} on |ff<-l| (|ff__id|, |__index| % 2)'\
            .format(quote(indexee.name))
        qAct = As(Index)(index).createQuery(quote)
        self.assertEqual(qExp, qAct)

    def test_mod(self):
        index = {
            'table': 'ff<-l',
            'parts': [
                ['mod(', ['__index', Index.quote], ' , 2)'],
            ]
        }

        indexee = As(Index)(index)
        def quote(c): return '|{}|'.format(c)
        qExp = 'create index if not exists {} on |ff<-l| (mod(|__index| , 2))'\
            .format(quote(indexee.name))
        qAct = As(Index)(index).createQuery(quote)
        self.assertEqual(qExp, qAct)


if __name__ == '__main__':

    unittest.main()
