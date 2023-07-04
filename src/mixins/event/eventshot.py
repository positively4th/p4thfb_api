import ramda as R

from contrib.pyas.src.pyas_v3 import Leaf


class EventShot(Leaf):

    prototypes = []

    freeKickTypeId = '62'
    openPlay = '87'
    penaltyTypeId = '88'

    bodyPartId = {
        'head': '37',
        'leftFoot': '38',
        'other': '70',
        'rightFoot': '40',
    }

    idTypeMap = {
        '62': 'Free Kick',
        '87': 'Open Play',
        '88': 'Penalty',
    }

    typeIdMap = {v: k for k, v in idTypeMap.items()}


if __name__ == "__main__":
    pass
