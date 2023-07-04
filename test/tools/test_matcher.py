import unittest

from src.tools.matcher import Matcher


class TestMatcher(unittest.TestCase):

    @classmethod
    def eq(cls, n):
        return lambda x: x == n

    @classmethod
    def geq(cls, n):
        return lambda x: x >= n

    @classmethod
    def leq(cls, n):
        return lambda x: x <= n

    def test_one(self):
        self.assertTrue(Matcher.isMatch(5, self.eq(5)))

    def test_flat_and(self):
        self.assertTrue(Matcher.isMatch(5, [
            self.geq(4),
            '&',
            self.leq(6),
        ]))

        self.assertFalse(Matcher.isMatch(5, [
            self.geq(6),
            '&',
            self.leq(6),
        ]))

        self.assertFalse(Matcher.isMatch(5, [
            self.geq(4),
            '&',
            self.leq(4),
        ]))

        self.assertFalse(Matcher.isMatch(5, [
            self.geq(6),
            '&',
            self.leq(4),
        ]))

    def test_flat_or(self):
        self.assertTrue(Matcher.isMatch(5, [
            self.geq(4),
            '|',
            self.leq(6),
        ]))

        self.assertTrue(Matcher.isMatch(5, [
            self.geq(6),
            '|',
            self.leq(6),
        ]))

        self.assertTrue(Matcher.isMatch(5, [
            self.geq(4),
            '|',
            self.leq(4),
        ]))

        self.assertFalse(Matcher.isMatch(5, [
            self.geq(6),
            '|',
            self.leq(4),
        ]))

    def test_deep_and_or(self):
        self.assertTrue(Matcher.isMatch(5, [
            self.geq(4),
            '&',
            [
                self.leq(6),
                '|',
                self.leq(4),
            ],
        ]))

        self.assertFalse(Matcher.isMatch(5, [
            self.geq(6),
            '&',
            [
                self.leq(6),
                '|',
                self.leq(4),
            ],
        ]))

        self.assertFalse(Matcher.isMatch(5, [
            self.geq(4),
            '&',
            [
                self.leq(4),
                '|',
                self.leq(4),
            ],
        ]))

    def test_matcher(self):
        subjects = [1, 2, 3, 4, 5]
        expected = [2, 3, 4]
        actual = Matcher.match(subjects, [self.geq(2), '&', self.leq(4)])
        self.assertEqual(expected, actual)

if __name__ == '__main__':

    unittest.main()
