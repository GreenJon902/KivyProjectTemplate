from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from lib.betterLogger import BetterLogger


class APP_NAME_ScreenManager(ScreenManager, BetterLogger):
    def set_screen(self, screen_name):
        print(screen_name)
        print(self.screens)
        self.current = screen_name

        self.log_info("Switched to " + str(screen_name))


def get_sm() -> APP_NAME_ScreenManager:
    BetterLogger().log_deep_debug("get_sm(): Returning screen manager")
    return App.get_running_app().root.current


def get_screen(screen_name: str) -> Screen:
    return get_sm().get_screen(screen_name)


__all__ = ["APP_NAME_ScreenManager", "get_sm", "get_screen"]
