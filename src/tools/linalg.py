import numpy as np

class LinAlg:

    @classmethod
    def transform(cls, p, *args ):
        Tp = p
        for T in args:
            Tp = np.matmul(T, Tp)
        return Tp

    
    @classmethod
    def normalize(cls, a):
        return np.multiply(1.0 / np.linalg.norm(a), a)

    @classmethod
    def orthogonal(cls, a, clockwise=True):
        b = np.zeros(len(a))
        b[0] = a[1] * (1.0 if clockwise else -1.0)
        b[1] = a[0] * (-1.0 if clockwise else 1.0)
        return b
    
    @classmethod
    def rayRayIntersection(cls, p0, dp, q0, dq):
        
        D = np.identity(3)
        D[:,0] = dp
        D[:,1] = dq

        d = np.linalg.det(D)

        if d == 0:
            return None

        N = np.identity(3)
        N[:,0] = np.subtract(q0, p0)

        N[:,1] = dq
        p = np.linalg.det(N) / d

        N[:,1] = dp
        q = np.linalg.det(N) / d

        return p, q

    @classmethod
    def isInInteriorAngleArea(cls, p, s, da, db):
        # https: // www.mathcha.io/editor/Q0Xy9FM8fqNU0KNrqwtYO0odgfMweY4qhEXo90Y

        d = np.subtract(p, s)
        r = cls.orthogonal(d)

        phiAlpha = np.matmul(
            np.linalg.inv(np.column_stack((r, np.multiply(-1, da), [0, 0, 1]))),
            np.subtract(s, p)
        )

        thetaBeta = np.matmul(
            np.linalg.inv(np.column_stack((r, np.multiply(-1, db), [0, 0, 1]))),
            np.subtract(s, p)
        )

        return phiAlpha[1] > 0 and thetaBeta[1] > 0 and phiAlpha[0] * thetaBeta[0] <= 0
