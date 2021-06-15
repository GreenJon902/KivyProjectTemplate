import os
import appdirs

appname: str = "APP_INFO_"
appauthor: str = "AUTHOR"
version: str = "VERSION"
roaming: bool = False

array: {str: any} = {"appname": appname,
                     "appauthor": appauthor,
                     "version": version,
                     "roaming": roaming}

AppDirs: appdirs.AppDirs = appdirs.AppDirs(**array)

user_data_dir: str = AppDirs.user_data_dir
kivy_home_dir: str = os.path.join(user_data_dir, "kivy")
config_dir: str = os.path.join(user_data_dir, "config")
code_dir: str = os.path.dirname(os.path.realpath(__file__))
resources_dir: str = os.path.join(code_dir, "ResourceFiles")
default_files_dir: str = os.path.join(resources_dir, "DefaultFiles")
default_settings_file: str = os.path.join(default_files_dir, "default_settings.json")
default_game_data_file: str = os.path.join(default_files_dir, "default_game_data.json")
settings_file: str = os.path.join(user_data_dir, "settings.json")
game_data_file: str = os.path.join(user_data_dir, "gameData.json")
texture_link_file: str = os.path.join(resources_dir, "textureLink.ini")
font_link_file: str = os.path.join(resources_dir, "fontLink.ini")
graphics_file: str = os.path.join(resources_dir, "graphicsConfig.ini")
kv_language_dir: str = os.path.join(resources_dir, "kv_language")
log_dir: str = AppDirs.user_log_dir
log_name: str = appname + "_%y-%m-%d_%_.log"
log_class_length: int = 48
pre_load_dir: str = os.path.join(resources_dir, "PreLoadResources")
pre_load_kv_lang_path: str = os.path.join(pre_load_dir, "pre_load_kv_lang.kv")

default_size: [int] = 700, 500

__all__ = ["appname", "appauthor", "version", "roaming",
           "array",
           "user_data_dir", "kivy_home_dir", "config_dir", "code_dir", "default_settings_file", "settings_file",
           "log_dir", "resources_dir", "texture_link_file", "kv_language_dir", "graphics_file", "font_link_file",
           "default_size", "log_name", "log_class_length", "game_data_file"]
