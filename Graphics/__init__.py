import ntpath
import os

from kivy.core.window import Window
from kivy.logger import Logger
from kivy.factory import Factory
from kivy.lang import Builder

import AppInfo
from graphics.APP_NAME_app import APP_NAME_App


def size() -> tuple[int, int]:  # because it might have adverts or something, idk
    return width(), height()


def width() -> int:  # because it might have adverts or something, idk
    return Window.width


def height() -> int:  # because it might have adverts or something, idk
    return Window.height


def load_kv():
    for filename in os.listdir(AppInfo.kv_language_dir):
        Logger.debug("kv_loader: Loading " + str(filename))
        Builder.load_file(os.path.join(AppInfo.kv_language_dir, filename))
        Logger.debug("kv_loader: Loaded " + str(filename))


def load_pre_load_kv():
    path: str = AppInfo.pre_load_kv_lang_path
    Logger.debug("kv_loader: Loading " + str(ntpath.basename(path)))
    Builder.load_file(path)
    Logger.debug("kv_loader: Loaded " + str(ntpath.basename(path)))


def setup():
    from graphics import APP_NAME_screenManager
    from graphics.screens.exampleScreen import ExampleScreen
    from graphics.customWidgets.screenManagerSwitcher import ScreenManagerSwitcher
    from graphics.APP_NAME_screenManager import APP_NAME_ScreenManager
    from graphics.preLoadScreenManager import PreLoadScreenManager
    from graphics.screens.splashScreen import SplashScreen
    from graphics.screens.loadingScreen import LoadingScreen
    from graphics.customWidgets.multiLangLabel import MultiLangLabel

    Factory.register("DrawSwapScreenManager", cls=APP_NAME_screenManager)
    Factory.register("ExampleScreen", cls=ExampleScreen)
    Factory.register("ScreenManagerSwitcher", cls=ScreenManagerSwitcher)
    Factory.register("APP_NAME_ScreenManager", cls=APP_NAME_ScreenManager)
    Factory.register("PreLoadScreenManager", cls=PreLoadScreenManager)
    Factory.register("SplashScreen", cls=SplashScreen)
    Factory.register("LoadingScreen", cls=LoadingScreen)
    Factory.register("MultiLangLabel", cls=MultiLangLabel)

    Logger.info("All classes have been assigned to Factory")


def start():
    Logger.info("Graphics are starting")

    app = APP_NAME_App()
    app.run()

    Logger.info("Graphics have ended")
