from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen

from graphics.preLoadScreenManager import get_sm


class SplashScreen(Screen):
    show_time: int = NumericProperty(1)

    def on_enter(self, *args):
        Clock.schedule_once(lambda *_elapsed_time: get_sm().set_screen("LoadingScreen"), self.show_time)
