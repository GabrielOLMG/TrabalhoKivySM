from configuracao import *
class Player:
    def __init__(self,nome):
        self.nome = nome
        self.karma = 0
        self.posicao = 35    
    def jogador_print(self):
        return f"Vez do Jogador {self.nome}\n"

    def info(self):
        return self.jogador_print() + f"Karma = {self.karma}\nPosicao = {self.posicao}"
    
    def controla_karma(self):
        if self.karma >= KARMA_MAXIMO_MINIMO:
            self.karma = KARMA_MAXIMO_MINIMO
        elif self.karma <= -KARMA_MAXIMO_MINIMO:
            self.karma = -KARMA_MAXIMO_MINIMO