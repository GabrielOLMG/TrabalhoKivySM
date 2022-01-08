from kivy.app import App 
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.config import Config
from kivy.animation import Animation
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.popup import Popup

from Cartas_class import *
from Jogo_class import *
from Jogador import *
from configuracao import *

#Config.set('graphics', 'resizable', False)

####################################################################################################
####################################################################################################

class MenuPrincipal(Screen):
    pass

class MenuSinglePlayer(Screen):
    pass  

class JogoTelaPrincipal(Screen):
    pass  

class JogoTelaMinigame(Screen):
    pass  

class JogoFinal(Screen):
    pass  

class Popups_costa(FloatLayout):
    pass

class Popups_frente(FloatLayout):
    pass

####################################################################################################
####################################################################################################

class mainApp(App):  
    jogadores = []
    a = NumericProperty(60)
    ativoC = False
    ativoF = False
    
    def build(self):
        self.screen_manager = ScreenManager(transition=NoTransition())
        self.screen_manager.add_widget(MenuPrincipal(name = "MenuPrincipal"))
        self.screen_manager.add_widget(MenuSinglePlayer(name = "MenuSinglePlayer"))
        self.screen_manager.add_widget(JogoTelaPrincipal(name = "JogoTelaPrincipal"))
        self.screen_manager.add_widget(JogoTelaMinigame(name = "JogoTelaMinigame"))
        self.screen_manager.add_widget(JogoFinal(name = "JogoFinal"))
        self.show_C = Popups_costa()
        self.show_F = Popups_frente()

        return self.screen_manager

    def reseta(self):
        self.jogadores = []
        self.screen_manager.get_screen("MenuSinglePlayer").ids.quantidade_jogadores.text = ""

        self.screen_manager.get_screen("MenuSinglePlayer").ids.ultimo_jogador_criado.text = ""

        self.screen_manager.get_screen("MenuSinglePlayer").ids.new_player_btn.disabled = False

        self.screen_manager.get_screen("MenuSinglePlayer").ids.jogar_btn.disabled = True
        self.screen_manager.get_screen("MenuSinglePlayer").ids.jogar_btn.opacity = 0

        self.screen_manager.get_screen("MenuSinglePlayer").ids.nome_player.disabled = False
        self.screen_manager.get_screen("MenuSinglePlayer").ids.nome_player.opacity = 1
        self.screen_manager.get_screen("MenuSinglePlayer").ids.nome_player.text = ""
        Animation.cancel_all(self)
        
        a = NumericProperty(60)
        self.posicao_vez = None
        self.jogador_vez = None

    def new_player(self,nome):
        player = Player(nome if nome != "" else "Jogador " + str(len(self.jogadores) + 1)) 
        self.jogadores.append(player)
        self.screen_manager.get_screen("MenuSinglePlayer").ids.quantidade_jogadores.text = "Jogando = " +  str(len(self.jogadores))
        self.screen_manager.get_screen("MenuSinglePlayer").ids.nome_player.text = ""
        self.screen_manager.get_screen("MenuSinglePlayer").ids.ultimo_jogador_criado.text = "Ultimo Jogador Criado = " + player.nome
        if len(self.jogadores) >= 3:
            self.screen_manager.get_screen("MenuSinglePlayer").ids.new_player_btn.disabled = True
            self.screen_manager.get_screen("MenuSinglePlayer").ids.nome_player.disabled = True
            self.screen_manager.get_screen("MenuSinglePlayer").ids.nome_player.opacity = 0
        else:
            self.screen_manager.get_screen("MenuSinglePlayer").ids.jogar_btn.disabled = False
            self.screen_manager.get_screen("MenuSinglePlayer").ids.jogar_btn.opacity = 1
        
        self.posicao_vez = 0
        self.jogador_vez = self.jogadores[self.posicao_vez] 

    def inicia_jogo(self):
        self.atualiza_info()
        self.jogo = Jogo()
        self.carta = Carta()
    
    def atualiza_info(self):
        self.screen_manager.get_screen("JogoTelaPrincipal").ids.info_player.text = self.jogador_vez.info()

    def inicia_round(self):
        self.screen_manager.get_screen("JogoTelaPrincipal").ids.Dado.disabled = False
        self.screen_manager.get_screen("JogoTelaPrincipal").ids.Dado.opacity = 1
        self.screen_manager.get_screen("JogoTelaPrincipal").ids.Turno.disabled = True

    def roda_dado(self):
        self.dado = random.randint(1,6)
        self.jogador_vez.posicao += self.dado + self.jogador_vez.karma
        if self.jogador_vez.posicao >=CASA_MAXIMA_MINIMA:
            self.lida_final_jogo(True) 
            return True
        elif -CASA_MAXIMA_MINIMA>self.jogador_vez.posicao:
            self.lida_final_jogo(False) 
            return True
        else:
            self.show_C.ids.carta_costa.text = f"Tendo tirado {self.dado} no dado com um\nKarma {self.jogador_vez.karma}, mova para a casa {self.jogador_vez.posicao}.\nVire a carta e veja o que te aguarda"
            self.status_posicao()
            self.atualiza_info()
            self.screen_manager.get_screen("JogoTelaPrincipal").ids.Dado.disabled = True
            return False
        
    def jogador_jogando(self,minigame = False,carta = False):
        if not minigame:
            if not self.roda_dado():
                self.ativa_desativa_popup_costa()            
        elif minigame and not carta:
            self.ativa_desativa_popup_costa()
            self.ativa_desativa_popup_frente()
        else:
            self.ativa_desativa_popup_frente()
            if self.efeito == None:
                self.prepara_minigame()
                self.screen_manager.current = 'JogoTelaMinigame'
            else:
                self.sai_minigame()

    def prepara_minigame(self):
        self.reseta_minigame()
        if self.minigame == "Perguntas":
            self.valores = self.jogo.Perguntas_Jogo()
        elif self.minigame == "Lixo":
            self.valores = self.jogo.Lixo_Jogo()
            self.screen_manager.get_screen("JogoTelaMinigame").ids.r3.pos_hint = {'center_y':.3, 'center_x':0.5 }
            self.screen_manager.get_screen("JogoTelaMinigame").ids.r4.opacity = 0
            self.screen_manager.get_screen("JogoTelaMinigame").ids.r4.disabled = True
        elif self.minigame == "Mimica":
            self.valores = self.jogo.Mimica_Jogo()
            
            self.mimica()
            
            return

        self.screen_manager.get_screen("JogoTelaMinigame").ids.pergunta.text = self.valores[0]
        self.screen_manager.get_screen("JogoTelaMinigame").ids.r1.text = self.valores[1]
        self.screen_manager.get_screen("JogoTelaMinigame").ids.r2.text = self.valores[2]
        self.screen_manager.get_screen("JogoTelaMinigame").ids.r3.text = self.valores[3]
        self.screen_manager.get_screen("JogoTelaMinigame").ids.r4.text = self.valores[4]

    def reseta_minigame(self):
        self.screen_manager.get_screen("JogoTelaMinigame").ids.r1.disabled = False
        self.screen_manager.get_screen("JogoTelaMinigame").ids.r1.opacity = 1
        self.screen_manager.get_screen("JogoTelaMinigame").ids.r1.pos_hint = {'center_y':.5, 'center_x':0.25 } 
        
        self.screen_manager.get_screen("JogoTelaMinigame").ids.r2.disabled = False
        self.screen_manager.get_screen("JogoTelaMinigame").ids.r2.opacity = 1
        self.screen_manager.get_screen("JogoTelaMinigame").ids.r2.pos_hint = {'center_y':.5, 'right':1 } 

        self.screen_manager.get_screen("JogoTelaMinigame").ids.r3.disabled = False
        self.screen_manager.get_screen("JogoTelaMinigame").ids.r3.opacity = 1
        self.screen_manager.get_screen("JogoTelaMinigame").ids.r3.pos_hint = {'center_y':.3, 'center_x':0.25  }

        self.screen_manager.get_screen("JogoTelaMinigame").ids.r4.disabled = False
        self.screen_manager.get_screen("JogoTelaMinigame").ids.r4.opacity = 1
        self.screen_manager.get_screen("JogoTelaMinigame").ids.r4.pos_hint = {'center_y':.3, 'right':1 } 

    def mimica(self):
        self.screen_manager.get_screen("JogoTelaMinigame").ids.pergunta.text = self.valores

        self.screen_manager.get_screen("JogoTelaMinigame").ids.r1.disabled = False
        self.screen_manager.get_screen("JogoTelaMinigame").ids.r1.opacity = 1
        self.screen_manager.get_screen("JogoTelaMinigame").ids.r1.text = "Iniciar"
        self.screen_manager.get_screen("JogoTelaMinigame").ids.r1.pos_hint = {'center_y':.5, 'center_x':.5 }
        

        self.screen_manager.get_screen("JogoTelaMinigame").ids.r2.disabled = True
        self.screen_manager.get_screen("JogoTelaMinigame").ids.r2.opacity = 0

        self.screen_manager.get_screen("JogoTelaMinigame").ids.r3.disabled = True
        self.screen_manager.get_screen("JogoTelaMinigame").ids.r3.opacity = 0
        
        self.screen_manager.get_screen("JogoTelaMinigame").ids.r4.disabled = True
        self.screen_manager.get_screen("JogoTelaMinigame").ids.r4.opacity = 0


    def resposta_minigame(self,resposta,mimica_ativado= False, resposta_mimica = False):
        print(self.minigame)
        if self.minigame != "Mimica" or not mimica_ativado:
            print("AQI")
            if resposta == self.valores[-1]:
                print("Acertou")
                self.jogador_vez.karma+=1
            else:
                print("Errou")
                self.jogador_vez.karma-=1
        else:
            if not resposta_mimica :
                self.screen_manager.get_screen("JogoTelaMinigame").ids.r1.disabled = True
                self.screen_manager.get_screen("JogoTelaMinigame").ids.r1.opacity = 0

                self.screen_manager.get_screen("JogoTelaMinigame").ids.r2.disabled = False
                self.screen_manager.get_screen("JogoTelaMinigame").ids.r2.text = "Meu Colega Acertou"
                self.screen_manager.get_screen("JogoTelaMinigame").ids.r2.pos_hint = {'center_y':.3, 'center_x':0.5 }
                self.screen_manager.get_screen("JogoTelaMinigame").ids.r2.opacity = 1

                self.screen_manager.get_screen("JogoTelaMinigame").ids.r3.disabled = False
                self.screen_manager.get_screen("JogoTelaMinigame").ids.r3.text = "Meu Colega Errou"
                self.screen_manager.get_screen("JogoTelaMinigame").ids.r3.pos_hint = {'center_y':.5, 'center_x':0.5 }
                self.screen_manager.get_screen("JogoTelaMinigame").ids.r3.opacity = 1
                return
            else:
                if resposta == 2:
                    print("Acertou")
                    self.jogador_vez.karma+=1
                else:
                    print("Errou")
                    self.jogador_vez.karma-=1
        self.sai_minigame()            

    def status_posicao(self):
        posicao = self.jogador_vez.posicao
        if posicao in CASAS_ESPECIAIS:
            self.efeito =  self.carta.sorteia_carta(self.jogador_vez.posicao//abs(self.jogador_vez.posicao))
            self.minigame = None
            regra = self.carta.aplica_efeito_carta(self.jogador_vez,self.efeito)
            carta = "Casa Especial"
        else:
            self.efeito = None
            self.minigame = self.jogo.escolhe_jogo()
            regra = self.jogo.regras(self.minigame)
            carta = f"Casa Minigame- {regra[0]}"
            regra = regra[1]


        self.show_F.ids.tipo_carta.text = f"{carta}"
        self.show_F.ids.regra_carta.text = f"{regra}"
        self.jogador_vez.controla_karma()
        self.atualiza_info()

    def ativa_desativa_popup_costa(self):
        if not self.ativoC:
            self.popupWindow_costa = Popup(title ="", content = self.show_C,size_hint =(None, None), size =(300, 500),separator_height = 0)
            self.popupWindow_costa.background = "fotos\Carta Verso.png"
            self.popupWindow_costa.open()
            self.ativoC = True
        else:
            self.popupWindow_costa.dismiss()
            self.ativoC = False

    def ativa_desativa_popup_frente(self):
        if not self.ativoF:
            self.popupWindow_frente = Popup(title ="", content = self.show_F, size_hint =(None, None),size =(300, 500),separator_height = 0)
            self.popupWindow_frente.background = "fotos\Carta Frente2.png"
            self.popupWindow_frente.open()
            self.ativoF = True
        else:
            self.popupWindow_frente.dismiss()
            self.screen_manager.current = "JogoTelaMinigame"
            self.ativoF = False

    def sai_minigame(self):
        self.screen_manager.get_screen("JogoTelaPrincipal").ids.Dado.disabled = True
        self.screen_manager.get_screen("JogoTelaPrincipal").ids.Dado.opacity = 0
        self.screen_manager.get_screen("JogoTelaPrincipal").ids.Turno.disabled = False
        self.screen_manager.current = 'JogoTelaPrincipal'
        
        self.posicao_vez = self.posicao_vez + 1 if (self.posicao_vez + 1) < len(self.jogadores) else 0
        self.jogador_vez = self.jogadores[self.posicao_vez] 
        self.jogador_vez.controla_karma()
        self.atualiza_info()
        self.show_C = Popups_costa()
        self.show_F = Popups_frente()
        
    def lida_final_jogo(self,vitoria):
        self.screen_manager.current = "JogoFinal"
        if vitoria:
            self.screen_manager.get_screen("JogoFinal").ids.fim.text = f"PARABENS, {self.jogador_vez.nome}. COM O SEU CONHECIMENTO, O MUNDO CONSEGUIU SER SALVO."
        else:
            self.screen_manager.get_screen("JogoFinal").ids.fim.text = f"INFELIZMENTE NÃO FOI DESTA VEZ, {self.jogador_vez.nome}.MAS NÃO DESISTA, AO POUCOS MUDE SUA ROTINA, \nPESQUISE MAIS FORMAS DE SALVAR O MUNDO E COM CERTEZA SERA VOCE \nA FAZER A DIFERENÇA DA PROXIMA VEZ ;)"

####################################################################################################
####################################################################################################

if __name__ == "__main__":
    root = mainApp() 
    root.run() 

####################################################################################################
####################################################################################################