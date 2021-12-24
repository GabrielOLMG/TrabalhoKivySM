class Player:
    def __init__(self,nome):
        self.nome = nome
        self.karma = 0
        self.posicao = 0
    
    def info(self):
        return f"Nome = {self.nome}\nKarma = {self.karma}\nPosicao = {self.posicao}"