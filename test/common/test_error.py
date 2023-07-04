import unittest
import math

from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As

from src.common.error import Error
from src.mixins.context.context import Context


class UOContext(Leaf):

    prototypes = [Context] + Context.prototypes

    columnSpecs = {
        'errorType': {
            'transformer': lambda val, key, classee: val if key in classee.row else 'Unary Operators',
        },
        'number': {
            'transformer': lambda val, key, classee: val if key in classee.row else 'None',
        },
    }

    @classmethod
    def onNew(cls, self):
        self['errorType'] = 'Unary Operators'
        instance = self['instance']
        if instance:
            self['number'] = instance['number']


class UnaryOperations(Leaf):

    prototypes = []

    columnSpecs = {
        'number': {
            'transformer': lambda val, key, classee: val if key in classee.row else 'None',
        },
    }

    @Error.errorize(ContextClasses=As(UOContext), prefix='Inverse')
    def inverse(self):
        return 1.0 / self['number']

    @Error.errorize(ContextClasses=As(UOContext), prefix='Inverse')
    def squareRoot(self):
        return math.sqrt(self['number'])


class TestError(unittest.TestCase):

    def test_method(self):

        uo = As(UnaryOperations)({'number': 2.0})
        self.assertEquals(0.5, uo.inverse())

        uo = As(UnaryOperations)({'number': 0.0})
        with self.assertRaises(Error) as cm:
            uo.inverse()
        self.assertEquals(
            'Inverse -> float division by zero', str(cm.exception))
        self.assertEquals('Unary Operators', cm.exception.context['errorType'])
        self.assertEquals(uo, cm.exception.context['instance'])
        self.assertEquals((), cm.exception.context['arguments'])
        self.assertEquals({}, cm.exception.context['argumentsMap'])
        self.assertEquals(0.0, cm.exception.context['number'])

    def test_property(self):

        uo = As(UnaryOperations)({'number': 4.0})
        self.assertEquals(2, uo.squareRoot())

        uo = As(UnaryOperations)({'number': -1.0})
        with self.assertRaises(Error) as cm:
            uo.squareRoot()
        self.assertEquals(
            'Inverse -> math domain error', str(cm.exception))
        self.assertEquals('Unary Operators', cm.exception.context['errorType'])
        self.assertEquals(uo, cm.exception.context['instance'])
        self.assertEquals((), cm.exception.context['arguments'])
        self.assertEquals({}, cm.exception.context['argumentsMap'])
        self.assertEquals(-1.0, cm.exception.context['number'])


if __name__ == '__main__':

    unittest.main()
