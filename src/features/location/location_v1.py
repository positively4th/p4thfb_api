from src.features.feature_v1 import Feature
from features.location.location import Location as Location0


class Location:

    prototypes = [Location0] + Location0.prototypes + \
        [Feature] + Feature.prototypes
