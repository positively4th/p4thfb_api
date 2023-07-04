from contrib.pyas.src.pyas_v3 import Leaf


class XYTestEvent(Leaf):
    pass


def createXYTestFeature(name, xy, column):

    class TestFeature(Leaf):

        @property
        async def value(self):
            return self.row[xy][column]

    return type(xy + str(column),  (TestFeature,), {})
