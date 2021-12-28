class Player:
    def __init__(self,nome):
        self.nome = nome
        self.karma = 0
        self.posicao = 0
        self.dado = None
    
    def jogador_print(self):
        return f"Vez do Jogador {self.nome}\n"

    def info(self):
        return self.jogador_print() + f"Karma = {self.karma}\nPosicao = {self.posicao}\nDado = {self.dado} "
    
    def controla_karma(self):
        if self.karma > 3:
            self.karma = 3
        elif self.karma < -3:
            self.karma = -3