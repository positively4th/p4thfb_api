class ClassIdentified:

    prototypes = []

    def approveVersion(semanticVersion: tuple):
        return semanticVersion[0] in [2, 3]

    @staticmethod
    def id(cls):
        if isinstance(cls, ClassIdentified):
            return ClassIdentified.id(cls.__class__)
        if hasattr(cls, 'id') and cls.id != ClassIdentified.id:
            return cls.id(cls)
        return cls.__name__
