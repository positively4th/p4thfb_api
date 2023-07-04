
import numpy as np

from constants.statsbombpitch import StatsBombPitch as SBP

sbpTpitch = [
        [0, -1, 0],
        [1,  0, 0],
        [0,  0, 1],
    ]

class Pitch:

    sbpTpitch = sbpTpitch
    pitchTsbp = np.linalg.inv(sbpTpitch)

    inf = np.matmul(sbpTpitch, SBP.inf)
    sup = np.matmul(sbpTpitch, SBP.sup)
    ext = np.matmul(sbpTpitch, SBP.ext)
    
