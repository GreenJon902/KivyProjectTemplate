from kivy.app import App
from kivy.core.window import Window

from Graphics.[appName]ScreenManager import [AppName]ScreenManager


class [AppName]App(App):
    def build(self):
        return [AppName]ScreenManager()
