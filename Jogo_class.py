from configuracao import *
from processa_input import perguntas,mimica
import random
class Jogo:
    lista_jogos = ["Mimica","Perguntas","Lixo"]
    lista_perguntas = perguntas()
    lista_mimicas = mimica()

    def escolhe_jogo(self):
        return self.lista_jogos[random.randint(0,len(self.lista_jogos)-1)]
    
    def regras(self,minigame):
        if minigame == "Perguntas":
            return PERGUNTAS_REGRA
        elif minigame == "Mimica":
            return MIMICA_REGRA
        elif minigame == "Lixo":
            return LIXO_REGRA
    
    def Perguntas_Jogo(self):
        posicao_pergunta = random.randint(0,len(self.lista_perguntas)-1)
        pergunta = self.lista_perguntas[posicao_pergunta]
        self.lista_perguntas.pop(posicao_pergunta)
        
        if len(self.lista_perguntas)==0: 
            self.lista_perguntas = perguntas()
        
        return (pergunta[0], pergunta[1], pergunta[2], pergunta[3], pergunta[4],int(pergunta[5]))
    
    def Lixo_Jogo(self):
        lixos = [(AMARELO_SIM,AMARELO_NAO),(AZUL_SIM,AZUL_NAO),(VERDE_SIM,VERDE_NAO)] 
        escolhido = lixos.pop(random.randint(0,2))
        
        tipo_lixo = escolhido[0][0]
        correto = escolhido[0][1][random.randint(0,len(escolhido[0][1])-1)]
        errado1 = escolhido[1][random.randint(0,len(escolhido[1])-1)]
        errado2 = lixos[0][0][1][random.randint(0,len(lixos[0][0][1])-1)]
        
        possiveis = [correto,errado1,errado2]
        random.shuffle(possiveis)
        resposta_index = possiveis.index(correto)

        return (tipo_lixo,possiveis[0], possiveis[1], possiveis[2], "",resposta_index+1)

    def Mimica_Jogo(self):
        posicao_mimica = random.randint(0,len(self.lista_mimicas)-1)
        mimica_ = self.lista_mimicas[posicao_mimica]
        self.lista_mimicas.pop(posicao_mimica)
        if len(self.lista_mimicas)==0: 
            self.lista_mimicas = mimica()

        print(mimica_)
        return "Tente imitar:" + mimica_