from src.features.feature_v2 import Feature


class Wrightetal2011():

    prototypes = [Feature] + Feature.prototypes

    @classmethod
    def onNew(cls, self):
        self.row['citation'] = \
            '''Wright, Craig & Polman, Remco & Jones, Bryan & Sargeson, Lee. (2011). Factors Associated with Goals and Goal Scoring Opportunities in Professional Soccer. International Journal of Performance Analysis in Sport. 11. 438-449. 10.1080/24748668.2011.11868563.'''
