import unittest
from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As


class NodeError(Exception):
    pass


class _Skip:
    pass


Skip = _Skip()


def createNode(nodesKey='branches', leafKey='leaf'):

    def addProperty(cls, col):

        def getter(self):
            return self.row[col]

        def setter(self, val):
            self.row[col] = val

        setattr(cls, col, property(
            getter, setter))

    class Node(Leaf):

        Skip = Skip

        prototypes = []

        columnSpecs = {}

        def map(self, T=lambda node, *args: node, nodeFilterer=lambda branch, *args: branch):

            def _map(selfish):
                leaf = T(selfish.row)
                if isinstance(leaf, (list, tuple)):
                    leaf, bk = leaf
                else:
                    leaf = leaf
                    bk = nodesKey

                if leaf == Skip:
                    return Skip
                leaf = {k: v for k, v in leaf.items() if v is not Skip or k == bk}

                if bk in leaf:
                    if leaf[bk] == Skip:
                        del leaf[bk]
                    return nodeFilterer(leaf)
                branches = []
                if nodesKey in selfish and selfish[nodesKey] is not None:
                    for branch in selfish[nodesKey]:
                        branches.append(_map(As(Node)(branch)))

                branches = [b for b in branches if b !=
                            Skip and nodeFilterer(b) != Skip]
                if len(branches) > 0:
                    leaf[bk] = branches
                return leaf

            res = _map(self)
            if res == Skip:
                return
            return res

        def group(self, keyMaker):

            key = keyMaker(self.row)
            if key is not None:
                return {key: [self.row]}

            res = {}

            if nodesKey not in self.row:
                return res

            for branch in self[nodesKey]:
                delta = As(Node)(branch).group(keyMaker)
                for key, val in delta.items():
                    res[key] = [] if not key in res else res[key]
                    res[key] += val
            return res

        def collectLeaves(self):

            if leafKey in self.row:
                return self[leafKey]

            if nodesKey not in self.row:
                return None

            res = []
            for branch in self[nodesKey]:
                res.append(As(Node)(branch).collectLeaves())

            return res

        def first(self, matcher=lambda row: True):

            if matcher(self.row):
                return self.row

            if nodesKey not in self.row:
                return None

            for branch in self[nodesKey]:
                res = As(Node)(branch).first(matcher)
                if res is not None:
                    return res

            return None

    addProperty(Node, leafKey)
    addProperty(Node, nodesKey)
    Node.columnSpecs[leafKey] = {
        'transformer': lambda val, key, classee: val if key in classee.row else None,
    }
    Node.columnSpecs[nodesKey] = {
        'transformer': lambda val, key, classee: val if key in classee.row else None,
    }
    return Node


Node = createNode()
Node.Skip = _Skip()

if __name__ == "__main__":

    unittest.main()
