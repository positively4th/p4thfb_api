import numpy as np

from colour import Color as Colour


class Color:

    @classmethod
    def complement(cls, color):
        col = Colour(color)
        col = Colour(rgb=(1.0 - c for c in col.rgb))
        return col.get_hex_l()

    
