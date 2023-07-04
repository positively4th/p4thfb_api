from contrib.pyas.src.pyas_v3 import Leaf


class StoreMapperException(Exception):
    pass


class StoreMapper(Leaf):

    prototypes = []

    columnSpecs = {}

    indexes = []

    queries = {
    }

    def getDataQuery(self, __ids: tuple[str] | list[str]) -> tuple:
        raise StoreMapperException('Not implemented.')

    def dataQuery(self, __ids: tuple[str] | list[str]) -> tuple:
        qs = {**self.queries, }

        q, p = self.getDataQuery(__ids)
        return (q, p)
