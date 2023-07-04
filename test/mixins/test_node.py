import unittest
import numpy as np

from contrib.pyas.src.pyas_v3 import As

from src.mixins.node import createNode
from src.mixins.node import Skip


class TestNode(unittest.TestCase):

    def test_first(self):

        Tree = createNode(nodesKey='branches', leafKey='name')

        t = {
            'id': 't1',
            'name': 'n1',
            'branches': [
                {
                    'id': 't11',
                    'name': 'n11',
                    'branches': [
                        {
                            'id': 't111',
                            'name': 'n111',
                        },
                        {
                            'id': 't112',
                            'name': 'n112',
                        },
                    ]
                },
                {
                    'id': 't12',
                    'name': 'n12',
                    'branches': [
                        {
                            'id': 't121',
                            'name': 'n121',
                        },
                        {
                            'id': 't122',
                            'name': 'n122',
                        },
                    ]
                },
                {
                    'id': 't13',
                    'name': 'n13',
                    'branches': [
                        {
                            'id': 't153',
                            'name': 'n153',
                        },
                        {
                            'id': 't164',
                            'name': 'n164',
                        },
                    ]
                },
            ]
        }

        exp = None
        act = As(Tree)(t).first(lambda row: row['name'] == 'does not exist')
        self.assertEquals(exp, act)

        exp = {
            'id': 't12',
            'name': 'n12',
                    'branches': [
                        {
                            'id': 't121',
                            'name': 'n121',
                        },
                        {
                            'id': 't122',
                            'name': 'n122',
                        },
                    ]
        }

        act = As(Tree)(t).first(lambda row: row['id'] == 't12')
        self.assertEquals(exp, act)

    def test_collectLeaves(self):

        tree = {
            'n': 'root',
            'b': [],
        }
        for x in range(4):
            xyz = {
                'n': 'x',
                'b': [],
            }
            for y in range(3):
                yz = {
                    'n': 'y',
                    'b': [],
                }
                for z in range(2):
                    z = {
                        'n': 'z',
                        'l': int(str(x) + str(y) + str(z)),
                    }
                    yz['b'].append(z)

                xyz['b'].append(yz)

            tree['b'].append(xyz)

        xyzTree = As(createNode(nodesKey='b', leafKey='l'))(tree)
        nda = np.array(xyzTree.collectLeaves())
        for i1 in range(4):
            for i2 in range(3):
                for i3 in range(2):
                    assert nda[i1, i2, i3] == int(str(i1) + str(i2) + str(i3))

        xyz2Tree = xyzTree.map(lambda branch: ({
            'n': '{}2'.format(branch['n']),
            'l': branch['l'] + branch['l'] if 'l' in branch else Skip
        }, 'bb'))
        xyz2Tree = As(createNode(nodesKey='bb', leafKey='l'))(xyz2Tree)
        nda2 = np.array(xyz2Tree.collectLeaves())
        for i1 in range(4):
            for i2 in range(3):
                for i3 in range(2):
                    assert nda2[i1, i2, i3] == 2 * \
                        int(str(i1) + str(i2) + str(i3))

        xyTree = As(createNode(nodesKey='b', leafKey='l'))(tree)
        xyTree = xyTree.map(lambda b: {
            'n': b['n'],
            'l': b['b'][1]['l'] if b['n'] == 'y' else Skip,
        } if b['n'] != 'z' else Skip)
        xyTree = As(createNode(nodesKey='b', leafKey='l'))(xyTree)
        nda = np.array(xyTree.collectLeaves())
        for i1 in range(4):
            for i2 in range(3):
                assert nda[i1, i2] == int(str(i1) + str(i2) + str(1))

    def test_group(self):

        t = {
            'id': 't1',
            'name': 'n1',
            'branches': [
                {
                    'id': 't11',
                    'name': 'n11',
                    'branches': [
                        {
                            'id': 't111',
                            'name': 'n111',
                        },
                        {
                            'id': 't112',
                            'name': 'n112',
                        },
                    ]
                },
                {
                    'id': 't12',
                    'name': 'n12',
                    'branches': [
                        {
                            'id': 't121',
                            'name': 'n121',
                        },
                        {
                            'id': 't122',
                            'name': 'n122',
                        },
                    ]
                },
                {
                    'id': 't13',
                    'name': 'n13',
                    'branches': [
                        {
                            'id': 't153',
                            'name': 'n153',
                        },
                        {
                            'id': 't164',
                            'name': 'n164',
                        },
                    ]
                },
            ]
        }

        Tree = createNode(nodesKey='branches', leafKey='name')

        def oddEven100sKeyMaker(row):
            if not len(row['id']) == 4:
                return None
            if int(row['id'][-1]) % 2 == 1:
                return 'odd'
            return 'even'

        oddEven100s = As(Tree)(t).group(oddEven100sKeyMaker)
        # print(oddEven100s)
        self.assertEqual(2, len(oddEven100s))
        self.assertIn('odd', oddEven100s)
        self.assertIn('even', oddEven100s)

        expOdd = [
            {'id': 't111', 'name': 'n111'},
            {'id': 't121', 'name': 'n121'},
            {'id': 't153', 'name': 'n153'},
        ]
        self.assertEqual(expOdd, oddEven100s['odd'])
        expEven = [
            {'id': 't112', 'name': 'n112'},
            {'id': 't122', 'name': 'n122'},
            {'id': 't164', 'name': 'n164'},
        ]
        self.assertEqual(expEven, oddEven100s['even'])

    def test_map(self):

        t = {
            'id': 't1',
            'name': 'n1',
            'branches': [
                {
                    'id': 't11',
                    'name': 'n11',
                    'branches': [
                        {
                            'id': 't111',
                            'name': 'n111',
                        },
                        {
                            'id': 't112',
                            'name': 'n112',
                        },
                    ]
                },
                {
                    'id': 't12',
                    'name': 'n12',
                    'branches': [
                        {
                            'id': 't121',
                            'name': 'n121',
                        },
                        {
                            'id': 't122',
                            'name': 'n122',
                        },
                    ]
                },
                {
                    'id': 't13',
                    'name': 'n13',
                    'branches': [
                        {
                            'id': 't153',
                            'name': 'n153',
                        },
                        {
                            'id': 't164',
                            'name': 'n164',
                        },
                    ]
                },
            ]
        }

        Tree = createNode(nodesKey='branches', leafKey='name')

        def skip_t13(node):
            if node['id'] == 't13':
                return Skip
            return node

        def T(node):
            res = {**node}
            if 'branches' in res:
                del res['branches']
            return (res, 'bs')

        t = As(Tree)(t).map(T=T, nodeFilterer=skip_t13)
        self.assertEqual(t['id'], 't1')
        self.assertEqual(2, len(t['bs']))
        self.assertEqual(t['bs'][0]['id'], 't11')
        self.assertEqual(2, len(t['bs'][0]['bs']))
        self.assertEqual(t['bs'][1]['id'], 't12')
        self.assertEqual(2, len(t['bs'][1]['bs']))

        pass


if __name__ == '__main__':

    unittest.main()
