from xxhash import xxh32


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
        name = cls.__name__.split('_')[0]
        return '{}_{}'.format(name, xxh32(cls.__name__).hexdigest())
