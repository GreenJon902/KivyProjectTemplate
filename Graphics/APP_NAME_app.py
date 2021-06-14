from kivy.app import App
from kivy.factory import Factory
from kivy.uix.screenmanager import Screen

from graphics.APP_NAME_screenManager import APP_NAME_ScreenManager
from lib.betterLogger import BetterLogger
from lib.saveManager import SaveManager
from resources import Lang


class APP_NAME_App(App, BetterLogger):
    sm: APP_NAME_ScreenManager = None

    def on_sm(self):
        self.sm.bind(on_current=self.on_screen_change)

    def build(self) -> APP_NAME_ScreenManager:
        self.log_info("Building app")

        return Factory.ScreenManagerSwitcher()

    def on_screen_change(self, new_screen: Screen):
        self.title = Lang.get("General.Title") + " - " + str(new_screen.name)

    def on_stop(self):
        SaveManager.end_clock()

    def on_start(self):
        SaveManager.start_clock()
