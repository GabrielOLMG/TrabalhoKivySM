import random
class Jogo:
    lista_jogos = ["Perguntas", "Mimica", "Lixo"]
    
    def escolhe_jogo(self):
        return self.lista_jogos[random.randint(0,len(self.lista_jogos)-1)]