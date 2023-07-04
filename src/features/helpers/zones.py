from contrib.pyas.src.pyas_v3 import Leaf
from constants.statsbombpitch import StatsBombPitch as SBP


def coalesce(*args):
    args = list(args)
    while len(args) > 0:
        res = args.pop(0)
        if res is not None:
            return res
    return None


def createZone(sbInf, sbSup):

    class Zone(Leaf):
        prototypes = []

        clockWiseZonePoints = [
            [coalesce(sbInf[0], SBP.sbLeftOwnCorner[0]), coalesce(
                sbInf[1], SBP.sbLeftOwnCorner[1]), 1],
            [coalesce(sbInf[0], SBP.sbLeftOwnCorner[0]), coalesce(
                sbSup[1], SBP.sbRightOppCorner[1]), 1],
            [coalesce(sbSup[0], SBP.sbRightOppCorner[0]), coalesce(
                sbSup[1], SBP.sbRightOppCorner[1]), 1],
            [coalesce(sbSup[0], SBP.sbRightOppCorner[0]),
             coalesce(sbInf[1], SBP.sbLeftOwnCorner[1]), 1],
        ]

        @classmethod
        def onNew(cls, self):
            assert sbSup[0] >= sbInf[0] or (sbSup[0] is None or sbInf[0] is None),\
                'Invalid longitudinal inf/sup for zone.'
            assert sbSup[1] >= sbInf[1] or (sbSup[1] is None or sbSup[1] is None),\
                'Invalid lateral inf/sup for zone.'

        @classmethod
        def isInZone(cls, p):
            return (sbInf[0] is None or p[0] >= sbInf[0]) \
                and (sbInf[1] is None or p[1] > sbInf[1]) \
                and (sbSup[0] is None or p[0] < sbSup[0]) \
                and (sbSup[1] is None or p[1] <= sbSup[1])
            # return not (p[0] < sbInf[0] or p[1] < sbInf[1] or p[0] >= sbSup[0] or p[1] >= sbSup[1])

    return Zone


laDividers = [
    SBP.sbLeftOwnCorner[1] - 0.01 * (SBP.sbSup[1] - SBP.sbInf[1]),
    0.5 * SBP.sbLeftOppPenaltyAreaCross[1],
    SBP.sbLeftOwnGoalAreaCross[1],
]
laDividers += [SBP.sbSup[1] - x for x in reversed(laDividers)]

loDividers = [
    SBP.sbLeftOwnCorner[0] - 0.01 * (SBP.sbSup[0] - SBP.sbInf[0]),
    SBP.sbLeftCenterLineCross[0],
    SBP.sbLeftOppPenaltyAreaCorner[0],
    SBP.sbSup[0] - 0.5 * (SBP.sbSup[0] - SBP.sbLeftOppPenaltyAreaCorner[0]),
    SBP.sbSup[0] + 0.01 * (SBP.sbSup[0] - SBP.sbInf[0]),
]

Zone8 = createZone((loDividers[0], laDividers[0], 1),
                   (loDividers[1], laDividers[5], 1))

Zone6 = createZone((loDividers[1], laDividers[0], 1),
                   (loDividers[4], laDividers[1], 1))
Zone5 = createZone((loDividers[1], laDividers[1], 1),
                   (loDividers[2], laDividers[4], 1))
Zone7 = createZone((loDividers[1], laDividers[4], 1),
                   (loDividers[4], laDividers[5], 1))


Zone2 = createZone((loDividers[2], laDividers[1], 1),
                   (loDividers[3], laDividers[4], 1))


Zone3 = createZone((loDividers[3], laDividers[1], 1),
                   (loDividers[4], laDividers[2], 1))
Zone4 = createZone((loDividers[3], laDividers[2], 1),
                   (loDividers[4], laDividers[3], 1))
Zone1 = createZone((loDividers[3], laDividers[3], 1),
                   (loDividers[4], laDividers[4], 1))


Zone6Yard = createZone(
    (SBP.sbLeftOppGoalAreaCorner[0], SBP.sbLeftOppGoalAreaCorner[1], 1),
    (SBP.sbRightOppGoalAreaCross[0], SBP.sbRightOppGoalAreaCross[1], 1)
)

Zone18Yard = createZone(
    (SBP.sbLeftOppPenaltyAreaCorner[0], SBP.sbLeftOppPenaltyAreaCorner[1], 1),
    (SBP.sbRightOppPenaltyAreaCross[0], SBP.sbRightOppPenaltyAreaCross[1], 1)
)

ZonePitch = createZone(
    (None, None, 1),
    (None, None, 1)
)
