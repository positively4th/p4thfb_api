from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As
from src.mixins.classidentified import ClassIdentified


class ClassNamed:

    prototypes = [ClassIdentified] + ClassIdentified.prototypes

    @staticmethod
    def name(cls):
        if hasattr(cls, 'name') and cls.name != ClassNamed.name:
            return cls.name(cls)
        if isinstance(cls, ClassNamed):
            return ClassNamed.name(cls.__class__)
        name = ClassIdentified.id(cls)
        name = name.split('_')
        return name[0]
