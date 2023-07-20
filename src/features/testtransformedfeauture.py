import unittest
from contrib.pyas.src.pyas_v3 import As
from src.features.transformedfeature import T
from src.features.feature_v1 import Feature


class TestTransformedFeature(unittest.TestCase):

    def test_Negate(self):
        from features.one_v1 import One

        MinusOne = As(T(One, 'MinusOne', lambda val, *
                      args: None if val is None else -val, id="minus_one"))
        minusOne = MinusOne()

        self.assertAlmostEqual(-1.0, minusOne.value, delta=0.000001)
        self.assertEqual('MinusOne', As(Feature).featureName(minusOne))
        self.assertEqual('minus_one', As(Feature).featureId(minusOne))


if __name__ == '__main__':

    unittest.main()
