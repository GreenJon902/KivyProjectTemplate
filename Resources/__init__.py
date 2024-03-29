import json
import os
from configparser import ExtendedInterpolation

from kivy.core.audio import SoundLoader
from kivy.core.image import Image as CoreImage
from kivy.core.text import LabelBase
from kivy.lang import Builder

import AppInfo
from AppInfo import resources_dir
from lib.ConfigParsers import PathConfigParser, JSONParser
from lib.betterLogger import BetterLogger
from resources.audio import Audio
from resources.gameConfig import GameConfig
from resources.lang import Lang
from resources.textures import Textures

current_threaded_tasks = list()


class ResourceLinks(BetterLogger):
    audio: PathConfigParser = PathConfigParser(interpolation=ExtendedInterpolation())
    font: PathConfigParser = PathConfigParser(interpolation=ExtendedInterpolation())
    language: PathConfigParser = PathConfigParser(interpolation=ExtendedInterpolation())
    texture: PathConfigParser = PathConfigParser(interpolation=ExtendedInterpolation())
    gameConfig: PathConfigParser = PathConfigParser(interpolation=ExtendedInterpolation())

    audio_file_name: str = "audioLink.ini"
    font_file_name: str = "fontLink.ini"
    language_file_name: str = "langLink.ini"
    texture_file_name: str = "textureLink.ini"
    game_data_file_name: str = "gameConfigLink.ini"

    array: {str: PathConfigParser} = {
        "audio": audio,
        "font": font,
        "language": language,
        "texture": texture,
        "gameConfig": gameConfig}

    def __init__(self, *args, **kwargs):
        BetterLogger.__init__(self, *args, **kwargs)
        self.audio.__log_name_prefix__ = "Audio_"
        self.font.__log_name_prefix__ = "Font_"
        self.language.__log_name_prefix__ = "Language_"
        self.texture.__log_name_prefix__ = "Textures_"
        self.gameConfig.__log_name_prefix__ = "GameConfig_"

    def load_link_files(self):
        self.log_debug("Loading link files")

        self.audio.read(os.path.join(resources_dir, self.audio_file_name))
        self.font.read(os.path.join(resources_dir, self.font_file_name))
        self.language.read(os.path.join(resources_dir, self.language_file_name))
        self.texture.read(os.path.join(resources_dir, self.texture_file_name))
        self.gameConfig.read(os.path.join(resources_dir, self.game_data_file_name))

        self.log_info("Loaded link files")


ResourceLinks: ResourceLinks = ResourceLinks()


class ResourceLoader(BetterLogger):
    # INFO:
    # We have deal resources and load separate increase we have duplicate resources so
    # then we only load it once and its simpler that way 
    paths_to_resources: dict[str, any] = {}
    tasks_completed: int = -1
    total_links: int = 0
    kv_files: int = 0
    tasks: list[dict[str, any]] = list()

    @property
    def number_of_tasks_to_do(self) -> int:
        return len(self.tasks) \
               + 1  # +1 is order task list

    @property
    def next_task_info(self) -> dict[any, any]:
        return self.tasks[self.tasks_completed]

    def get_tasks(self):
        ResourceLinks.load_link_files()
        self.get_paths()
        self.get_kv_files()

    def get_kv_files(self):
        self.__log_name_suffix__ = "_kv_lang"
        self.log_info("Starting to get all kv_file paths")

        for file in os.listdir(AppInfo.kv_language_dir):
            path = os.path.join(AppInfo.kv_language_dir, file)
            self.log_deep_debug("Found file", file, " Path is", path)

            self.tasks.append({
                "type": "load_kv_lang",
                "path": path
            })
            self.log_deep_debug("Appended to list")

        self.log_info("Finished getting all kv_file paths")
        self.__log_name_suffix__ = ""

    def get_paths(self):
        self.log_info("Starting to get all paths")

        self.tasks.append({
            "type": "load_resource",
            "resource_type": "mtlFile",
            "path": os.path.join(AppInfo.resources_dir, "materials.mtl")
        })

        """self.tasks.append({
            "type": "deal_resource",
            "resource_type": "mtlFile",
            "path": os.path.join(AppInfo.resources_dir, "materials.mtl")
        })"""
        self.total_links += 1

        for link_name in ResourceLinks.array:
            self.__log_name_suffix__ = "_" + str(link_name)
            link: PathConfigParser = ResourceLinks.array[link_name]
            self.log_debug("Loading paths from", link_name, link)

            for section in link.sections():
                for option in link.options(section):
                    self.log_deep_debug("Getting path from |", section, "|", option, "...")
                    path: str = link.get(section, option)
                    self.log_deep_debug("Path is", path)

                    self.total_links += 1

                    if link_name not in ["font"]:
                        if path not in self.paths_to_resources:
                            self.paths_to_resources[path] = None
                            self.tasks.append({
                                "type": "load_resource",
                                "resource_type": link_name,
                                "path": path
                            })
                            self.log_deep_debug("Appended to list")
                        else:
                            self.log_deep_debug("Already in list, no changes!")
                        self.tasks.append({
                            "type": "deal_resource",
                            "resource_type": link_name,
                            "section": section,
                            "option": option,
                            "path": path
                        })

                    elif link_name == "font":
                        self.tasks.append({
                            "type": "load_resource",
                            "resource_type": link_name,
                            "section": section,
                            "option": option,
                            "path": path
                        })
                        self.log_deep_debug("Appended to list")

                    else:
                        self.log_critical("Link name ib first sort exclusion list isn't sorted -", link_name)

        self.log_deep_debug()

        self.__log_name_suffix__ = ""
        self.log_info("Finished getting all paths")
        self.log_info(self.total_links, "links found")

    # def load_resource_from_path(self, path: str):
    #   time.sleep(1)

    def run_next_task(self) -> bool:
        # self.load_resource_from_path(str(self.paths_to_resources[list(self.paths_to_resources.keys())[self.paths_loaded]]))

        if self.tasks_completed == -1:  # order task list
            self.log_deep_debug("Ordering task list")

            correct_order_of_tasks: list[dict] = [{"type": "load_resource", "resource_type": "texture"},
                                                  {"type": "deal_resource", "resource_type": "texture"},

                                                  {"type": "load_resource", "resource_type": "language"},
                                                  {"type": "deal_resource", "resource_type": "language"},

                                                  {"type": "load_resource", "resource_type": "font"},

                                                  {"type": "load_resource", "resource_type": "audio"},
                                                  {"type": "deal_resource", "resource_type": "audio"},

                                                  {"type": "load_resource", "resource_type": "gameConfig"},
                                                  {"type": "deal_resource", "resource_type": "gameConfig"},

                                                  {"type": "load_kv_lang"}]
            """{"resource_type": "texture", "resource_type": "mtlFile",
                                                      "resource_type": "model", "resource_type": "language",
                                                      "resource_type": "audio", "resource_type": "fonts",
                                                      "deal_resource": "type", "load_kv_lang": "type"}"""
            new_tasks_list: list[dict[str, any]] = list()

            for types in correct_order_of_tasks:


                for task in self.tasks:
                    try:
                        correct = True
                        for t in types:
                            if not task[t] == types[t]:
                                correct = False
                                break

                        if correct:
                            new_tasks_list.append(task)

                        else:
                            pass
                    except KeyError:  # not in so dw
                        pass

            self.tasks = new_tasks_list

            self.log_deep_debug("Ordered task list -\n", str(self.tasks).replace("}, {", "},\n {"))

        else:  # Task list is ordered
            self.log_deep_debug("Doing next task. Number is", self.tasks_completed)

            self.run_task(self.tasks[self.tasks_completed])

        self.tasks_completed += 1
        if self.tasks_completed == self.number_of_tasks_to_do - 1:  # is done | -1 bc we need to order
            return True
        else:
            return False

    def run_task(self, task_info):
        self.__log_name_suffix__ = " | " + str(task_info["type"])
        self.log_deep_debug("Current task array is", task_info)

        if task_info["type"] == "load_resource":

            if task_info["resource_type"] == "language":
                file = open(task_info["path"] + ".json", "r")

                array = json.load(file)
                array = lang.convert(array)
                self.paths_to_resources[task_info["path"]] = array

                file.close()

            elif task_info["resource_type"] == "texture":
                core_image = CoreImage.load(task_info["path"])
                self.paths_to_resources[task_info["path"]] = core_image

            elif task_info["resource_type"] == "audio":
                sound = SoundLoader.load(task_info["path"])
                self.paths_to_resources[task_info["path"]] = sound

            elif task_info["resource_type"] == "font":
                LabelBase.register(name=task_info["section"] + "-" + task_info["option"],
                                   fn_regular=task_info["path"])
                self.log_deep_debug("Registered font -", task_info["path"], "for", task_info["section"] + "-" +
                                    task_info["option"])

            elif task_info["resource_type"] == "gameConfig":
                parser = JSONParser(task_info["path"])
                self.paths_to_resources[task_info["path"]] = parser

            else:
                self.log_critical("No know resource_type -", task_info["resource_type"])


        elif task_info["type"] == "deal_resource":
            if task_info["resource_type"] == "language":
                Lang.register_array(self.paths_to_resources[task_info["path"]], task_info["option"])

            elif task_info["resource_type"] == "texture":
                Textures.register(task_info["section"], task_info["option"], self.paths_to_resources[task_info["path"]])

            #  elif task_info["resource_type"] == "mtlFile":
            #    Models.register_materials(self.paths_to_resources[task_info["path"]])

            elif task_info["resource_type"] == "audio":
                Audio.register(task_info["option"], self.paths_to_resources[task_info["path"]])

            elif task_info["resource_type"] == "gameConfig":
                GameConfig.register(task_info["section"], task_info["option"],
                                    self.paths_to_resources[task_info["path"]])

            else:
                self.log_critical("No know resource_type -", task_info["resource_type"])

        elif task_info["type"] == "load_kv_lang":
            Builder.load_file(task_info["path"])

        else:
            self.log_critical("No know task type -", task_info["type"])

        self.__log_name_suffix__ = ""

    """loaded = {}

    def load_all(self):
        self.log_info("Starting to load all ResourceFiles")

        for link_name in ResourceLinks.array:
            self.log_debug("-"*100, "Loading from", link_name, "link", "-"*50)
            link = ResourceLinks.array[link_name]
            self.log_debug("Link ConfigParser is", link)

            for section in link.sections():
                for option in link.options(section):
                    self._load(link_name, section, option)

            self.log_debug("-"*100, "Finished loading from", link_name, "-"*50)
            # self.log_debug("\n")
            # self.log_debug("")

        self.log_info("-"*100, "Finished looping through resource files, waiting for threads to finish""-"*100)
        while len(current_threaded_tasks):
            self.log_trace("Threads left -", current_threaded_tasks)
        self.log_info("-"*100, "All threads finished!" + "-"*100)



    def _load(self, resource_type, section, option):
        self.__log_name_suffix__ = "___" + str(resource_type) + "__" + str(section) + "__" + str(option)
        self.log_debug("Loading", resource_type, "with the .ini path", (section, option))

        if resource_type not in self.loaded:
            self.loaded[resource_type] = {}

        if section not in self.loaded[resource_type]:
            self.loaded[resource_type][section] = {}

        if resource_type in self.loaded:
            if section in self.loaded[resource_type]:
                if option in self.loaded[resource_type][section]:
                    self.log_debug("Resource already loaded, skipping")

                else:
                    link = ResourceLinks.array[resource_type]
                    path = link.get(section, option)

                    self.log_debug("Got path -", path)

                    if resource_type == "language":
                        array = json.load(open(path + ".json", "r"))
                        self.log_debug(array)
                        Lang.register_array(array, option)

                        self.loaded[resource_type][section][option] = Lang.get_all(option)

                    if resource_type == "textures":
                        self.loaded[resource_type][section][option] = textures.load(path, section, option)


        # self.log_debug("")
        self.__log_name_suffix__ = """""


ResourceLoader: ResourceLoader = ResourceLoader()


__all__ = ["ResourceLoader", "Lang", "Textures", "Models", "GameConfig", "Audio", "ResourceLinks"]
