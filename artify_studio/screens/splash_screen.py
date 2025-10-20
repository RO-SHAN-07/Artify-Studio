from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

class SplashScreen(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(self.switch_to_home, 5)

    def switch_to_home(self, dt):
        self.manager.current = 'home'
