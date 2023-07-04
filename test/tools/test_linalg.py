import unittest
import numpy as np

from math import pi
from math import cos
from math import sin

from src.tools.linalg import LinAlg

class TestLinAlg(unittest.TestCase):

    def test_normalize(self):
        a = (6, -8, 0)
        n = LinAlg.normalize(a)
        self.assertAlmostEqual(np.linalg.norm(n), 1.0, 5)
        self.assertAlmostEqual(n[1] / n[0], -8.0 / 6.0, 5)

    def test_orthonogal(self):
        a = (6, -8, 0)
        n = LinAlg.orthogonal(a)
        self.assertAlmostEqual(np.linalg.norm(n), np.linalg.norm(a), 5)
        self.assertAlmostEqual(np.dot(a, n), 0.0, 5)


    def test_noRayRayIntersection(self):
        p = (1,1, 1)
        dp = (1,0, 0)
        actual = LinAlg.rayRayIntersection(p,dp, p, dp)
        self.assertIsNone(actual)

        p = (1,1, 1) 
        dp = (0,1, 0)
        q = (3,3, 1)
        dq = (0,1, 0)
        actual = LinAlg.rayRayIntersection(p,dp, q, dq)
        self.assertIsNone(actual)

    def test_orthoRayRayIntersection(self):

        def T(delta, alpha):
            rotT = np.identity(3)
            rotT[0,0] = np.cos(alpha)
            rotT[0,1] = np.sin(alpha)
            rotT[1,1] = np.cos(alpha)
            rotT[1,0] = -np.sin(alpha)

            traT = np.identity(3)
            traT[0,2] = delta[0] 
            traT[1,2] = delta[1]

            return np.matmul(traT, rotT)
            
        p = (0, 0, 1) 
        q = (0, 0, 1)
        dp = (1, 0, 0)
        dq = (0, 1, 0)
        actual = LinAlg.rayRayIntersection(p,dp, q, dq)
        self.assertAlmostEqual(actual[0], 0.0, 5)
        self.assertAlmostEqual(actual[1], 0.0, 5)

        p = (2, 0, 1) 
        q = (0, -3, 1)
        dp = (1, 0, 0)
        dq = (0, 1, 0)
        actual = LinAlg.rayRayIntersection(p,dp, q, dq)
        self.assertAlmostEqual(actual[0], -2.0, 5)
        self.assertAlmostEqual(actual[1], 3.0, 5)

        p = (2, 0, 1) 
        q = (0, -3, 1)
        dp = (4, 0, 0)
        dq = (0, 6, 0)
        actual = LinAlg.rayRayIntersection(p,dp, q, dq)
        self.assertAlmostEqual(actual[0], -0.5, 5)
        self.assertAlmostEqual(actual[1], 0.5, 5)

        
        transforms = [
            ([-5, 3, 0], 0.4 * 2 * pi),
            ([5, 3, 0], 0.4 * 2 * pi),
            ([-5, -3, 0], 0.4 * 2 * pi),
            ([5, -3, 0], 0.4 * 2 * pi),

            ([-5, 3, 0], 0.8 * 2 * pi),
            ([5, 3, 0], 0.8 * 2 * pi),
            ([-5, -3, 0], 0.8 * 2 * pi),
            ([5, -3, 0], 0.8 * 2 * pi),
        ]
        for args in transforms:
            actual = LinAlg.rayRayIntersection(
                np.matmul(T(*args), p),
                np.matmul(T(*args), dp),
                np.matmul(T(*args), q),
                np.matmul(T(*args), dq))
            self.assertAlmostEqual(actual[0], -0.5, 5)
            self.assertAlmostEqual(actual[1], 0.5, 5)
        
    def test_isInInteriorAngleArea(self):

        p0 = [0, 1, 1]
        q0 = [1, 1, 1]
        s0 = [0, 0, 1]
        a0 = [1, 2, 0]
        b0 = [-1, 2, 0]

        self.assertTrue(LinAlg.isInInteriorAngleArea(p0, s0, a0, b0))
        self.assertFalse(LinAlg.isInInteriorAngleArea(q0, s0, a0, b0))

        for i in range(0, 360, 10):
            delta = [
                float(i) if (i % 2) == 0 else float(-i),
                float(i) if (i % 3) > 0 else float(-i),
                0
            ]
            rad = 2 * float(i) / pi
            rotT = [
                [cos(rad), sin(rad), 0],
                [-sin(rad), cos(rad), 0],
                [0, 0, 1.0]
            ]
            traT = [
                [1, 0, delta[0]],
                [0, 1, delta[1]],
                [0, 0, 1],
            ]
            p = LinAlg.transform(p0, rotT, traT)
            q = LinAlg.transform(q0, rotT, traT)
            s = LinAlg.transform(s0, rotT, traT)
            a = LinAlg.transform(a0, rotT, traT)
            b = LinAlg.transform(b0, rotT, traT)
            self.assertTrue(LinAlg.isInInteriorAngleArea(p, s, a, b))
            self.assertFalse(LinAlg.isInInteriorAngleArea(q, s, a, b))

if __name__ == '__main__':

    unittest.main()
