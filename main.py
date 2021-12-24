from kivy.app import App 
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.config import Config
from Jogador import Player
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.progressbar import ProgressBar


Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '500')
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

#################################################  


##################################################

class mainApp(App):  
    jogadores = []
    a = NumericProperty(60)
    countdown = CountDown()
    
    def build(self):
        self.screen_manager = ScreenManager(transition=NoTransition())
        self.screen_manager.add_widget(MenuPrincipal(name = "MenuPrincipal"))
        self.screen_manager.add_widget(MenuSinglePlayer(name = "MenuSinglePlayer"))
        self.screen_manager.add_widget(JogoTelaPrincipal(name = "JogoTelaPrincipal"))
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

    def contador(self):
        Animation.cancel_all(self)  # stop any current animations
        self.anim = Animation(a=0, duration=self.a)
        def finish_callback(animation, incr_crude_clock):
            incr_crude_clock.text = "FINISHED"
        self.anim.bind(on_complete=finish_callback)
        self.anim.start(self)




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