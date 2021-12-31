from kivy.app import App 
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.config import Config
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from PIL import Image

from Cartas_class import *
from Jogo_class import *
from Jogador import *

#Config.set('graphics', 'width', '700')
#Config.set('graphics', 'height', '500')
Config.set('graphics', 'resizable', False)
###############################################

class CountDown(ProgressBar):
    e = []
    def count(self):
        if len(self.e) > 0: 
            for i in self.e:
                i.cancel()

        self.value = 60
        seconds = 60
        def count_it(seconds):
            if seconds == 0:
                return None
            seconds -= 1
            self.value = seconds
            self.e.append(Clock.schedule_once( lambda dt: count_it(seconds), 1))
        self.e.append(Clock.schedule_once( lambda dt: count_it(60), 1))
        print("fim")

###############################################
  
class MenuPrincipal(Screen):
    pass

class MenuSinglePlayer(Screen):
    pass  

class JogoTelaPrincipal(Screen):
    pass  

class JogoTelaMinigame(Screen):
    pass  

class Popups_costa(FloatLayout):
    pass

class Popups_frente(FloatLayout):
    pass
#################################################  


##################################################

class mainApp(App):  
    jogadores = []
    a = NumericProperty(60)
    countdown = CountDown()
    ativoC = False
    ativoF = False
    
    def build(self):
        self.screen_manager = ScreenManager(transition=NoTransition())
        self.screen_manager.add_widget(MenuPrincipal(name = "MenuPrincipal"))
        self.screen_manager.add_widget(MenuSinglePlayer(name = "MenuSinglePlayer"))
        self.screen_manager.add_widget(JogoTelaPrincipal(name = "JogoTelaPrincipal"))
        self.screen_manager.add_widget(JogoTelaMinigame(name = "JogoTelaMinigame"))
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

    def contador(self):
        Animation.cancel_all(self)  # stop any current animations
        self.anim = Animation(a=0, duration=self.a)
        def finish_callback(animation, incr_crude_clock):
            incr_crude_clock.text = "FINISHED"
        self.anim.bind(on_complete=finish_callback)
        self.anim.start(self)

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
        self.status_posicao()
        self.atualiza_info()
        self.screen_manager.get_screen("JogoTelaPrincipal").ids.Dado.disabled = True
        

    def jogador_jogando(self,minigame = False,carta = False):
        if not minigame:
            self.roda_dado() 
            self.ativa_desativa_popup_costa()
        elif minigame and not carta:
            self.ativa_desativa_popup_costa()
            self.ativa_desativa_popup_frente()
        else:
            self.ativa_desativa_popup_frente()
            self.screen_manager.current = 'JogoTelaMinigame'


            # if carta 

    def status_posicao(self):
        p = self.jogador_vez.posicao
        
        if p%2==0:
            self.jogador_vez.karma += 1
        elif p%3==0:
            efeito =  self.carta.sorteia_carta()
            self.carta.aplica_efeito_carta(self.jogador_vez,efeito)
            print(efeito)
        else:
            self.jogador_vez.karma -= 1
        self.jogador_vez.controla_karma()

    def ativa_desativa_popup_costa(self):
        if not self.ativoC:
            show = Popups_costa()
            self.popupWindow_costa = Popup(title ="", content = show,size_hint =(None, None), size =(300, 500),separator_height = 0)
            self.popupWindow_costa.background = "fotos\Carta Verso2.png"
            self.popupWindow_costa.open()
            self.ativoC = True
        else:
            self.popupWindow_costa.dismiss()
            self.ativoC = False

    def ativa_desativa_popup_frente(self):
        if not self.ativoF:
            show_F = Popups_frente()
            self.popupWindow_frente = Popup(title ="", content = show_F, size_hint =(None, None),size =(300, 500),separator_height = 0)
            self.popupWindow_frente.background = "fotos\Carta Frente2.png"
            self.popupWindow_frente.open()
            self.ativoF = True
        else:
            self.popupWindow_frente.dismiss()
            self.screen_manager.current = "JogoTelaMinigame"


##################################################

if __name__ == "__main__":
    root = mainApp() 
    root.run() 


'''
MenuPrincipal:
    - Botão: Jogo "Singleplayer"
    - Botão: Jogo "multiplayer" (com servidor cliente)

MenuSinglePlayer
'''
