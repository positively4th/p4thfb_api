import numpy as np


class StatsBombPitch:

    inf = [0, 0, 1]
    sup = [120, 80, 1]
    ext = np.subtract(sup, inf)

    sbInf = [0, 0, 1]
    sbSup = [120, 80, 1]
    sbLeftOwnCorner = (0, 0)
    sbLeftOwnPenaltyAreaCross = (0, 18)
    sbLeftOwnGoalAreaCross = (0, 30)
    sbLeftOwnGoalPost = (0, 36)
    sbRightOwnGoalPost = (0, sbSup[1] - 36)
    sbRightOwnGoalAreaCorner = (6, sbSup[1] - 30)
    sbRightOwnGoalAreaCross = (0, sbSup[1] - 30)
    sbRightOwnPenaltyAreaCorner = (18, sbSup[1] - 18)
    sbRightOwnPenaltyAreaCross = (0, sbSup[1] - 18)
    sbRightOwnCorner = (0, sbSup[1] - 360)

    sbLeftOwnGoalAreaCorner = (6, 30)
    sbOwnPenaltySpot = (12, 40)
    sbLeftOwnPenaltyAreaCorner = (18, 18)

    sbLeftCenterLineCross = (0.5 * (sbSup[0] + sbInf[0]), sbInf[1])
    sbRightCenterLineCross = (0.5 * (sbSup[0] + sbInf[0]), sbSup[1])

    sbLeftOppPenaltyAreaCorner = (sbSup[0] - 18, 18)
    sbOppPenaltySpot = (sbSup[0] - 12, 40)
    sbLeftOppGoalAreaCorner = (sbSup[0] - 6, 30)

    sbLeftOppCorner = (sbSup[0] - 0, 0)
    sbLeftOppPenaltyAreaCross = (sbSup[0] - 0, 18)
    sbLeftOppGoalAreaCross = (sbSup[0] - 0, 30)
    sbLeftOppGoalPost = (sbSup[0] - 0, 36)
    sbRightOppGoalPost = (sbSup[0] - 0, sbSup[1] - 36)
    sbRightOppGoalAreaCorner = (sbSup[0] - 6, sbSup[1] - 30)
    sbRightOppGoalAreaCross = (sbSup[0] - 0, sbSup[1] - 30)
    sbRightOppPenaltyAreaCorner = (sbSup[0] - 18, sbSup[1] - 18)
    sbRightOppPenaltyAreaCross = (sbSup[0] - 0, sbSup[1] - 18)
    sbRightOppCorner = (sbSup[0] - 0, sbSup[1] - 0)
