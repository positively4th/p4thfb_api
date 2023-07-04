import unittest

from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import Leaf

from src.features.feature_v2 import Feature


class TestFeature_v2(unittest.TestCase):

    def test_featureName(self):

        class A(Leaf):
            prototypes = [Feature] + Feature.prototypes

        self.assertEqual(Feature.featureName(As(A)), 'A')
        self.assertEqual(Feature.featureName(As(A)({})), 'A')
        self.assertEqual(Feature.featureName(As(A, Feature)), 'A')
        self.assertEqual(Feature.featureName(As(A, Feature)({})), 'A')


if __name__ == '__main__':

    unittest.main()
