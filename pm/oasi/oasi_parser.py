import json
import os

from simple_logger import Logger

import pm

__all__ = ["Settings", "Location"]


class Location:
    def __init__(self, dictionary):
        for key in ["name", "code", "coordinates"]:
            if key not in dictionary:
                raise RuntimeError("Key {} not in dictionary passed to "
                                   "Location.".format(key))
        self.name = dictionary["name"]
        self.code = dictionary["code"]
        self.coordinates = dictionary["coordinates"]

    def __repr__(self):
        return "OasiLocation ({})".format(self.code)

    def __str__(self):
        return "OasiLocation:" \
               "\n\t   name: {}" \
               "\n\t   code: {}" \
               "\n\t coords: {}".format(self.name, self.code, self.coordinates)


class Settings:
    def __init__(self, oasi_settings_file: str = None):
        if oasi_settings_file is None:
            oasi_settings_file = os.path.join(pm.Settings.resources_dir,
                                              "oasi_settings.json")
        self.settings_file = oasi_settings_file
        Logger.debug("Loading Oasi settings from {}".format(self.settings_file))

        self.__parse_settings_file()

    def __parse_settings_file(self) -> None:
        with open(self.settings_file, "r") as settings_file:
            parsed_settings = json.load(settings_file, object_hook=self.__settings_hook)

        if "locations" not in parsed_settings:
            raise RuntimeError("Could not load 'locations' key from parsed settings.")

        self.location_list = parsed_settings["locations"]

    @staticmethod
    def __settings_hook(dictionary: dict):
        if "coordinates" in dictionary:
            return Location(dictionary)
        else:
            return dictionary
