import random
from configuracao import *

class Carta:    
    
    def sorteia_carta(self,estado = 0):
        '''
            :param estado : 0->No meio do mapa, 1-> lado bom do mapa, -1-> lado ruim do mapa
        '''
        porcentagem = random.uniform(0, 1)
        print(porcentagem)
        if 0 <= porcentagem < 0.33 + (-2*estado/10): # se esta no lado bom, vai ter menos chance d somar karma
            return "Mais_Karma"
        elif 0.33 + (-2*estado/10) <= porcentagem < 0.66:
            return "Menos_Karma"
        elif 0.66 <= porcentagem < 0.99:
            return "Zera_Karma"
        else:
            return "Inverte_Karma"
    
    def aplica_efeito_carta(self,jogador,efeito):
        if efeito == "Mais_Karma":
            jogador.karma += 1
            jogador.controla_karma()
            return MAIS_KARMA
        elif efeito == "Menos_Karma":
            jogador.karma -= 1
            jogador.controla_karma()
            return MENOS_KARMA
        elif efeito == "Zera_Karma":
            jogador.karma = 0
            return ZERA_KARMA
        else:
            jogador.karma *=-1
            return INVERTE_KARMA



