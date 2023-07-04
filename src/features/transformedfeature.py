

def T(FeatureClass, name, T, id=None):

    _id = name if id is None else id

    class TransformedFeature:

        prototypes = [FeatureClass] + FeatureClass.prototypes

        @property
        def value(self):
            v = super().value
            return T(v)

        @classmethod
        def featureName(cls):
            return name

        @classmethod
        def featureId(cls):
            return id

    return TransformedFeature
