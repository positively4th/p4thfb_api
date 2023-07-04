

from src.features.feature_v2 import Feature
from src.constants.pitch import Pitch as P


class Location:

    prototypes = [Feature]

    pitchTcentric = [
        [1, 0, -0.5 * P.ext[0]],
        [0, 1, -0.5 * P.ext[1]],
        [0, 0, 1],
    ]
