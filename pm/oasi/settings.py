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
                                   "Location class.".format(key))
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


class Parameter:
    def __init__(self, dictionary: dict):
        for key in ["name", "code", "shortName", "unit"]:
            if key not in dictionary:
                raise RuntimeError("Key {} not in dictionary passed to "
                                   "Parameter class.".format(key))
        self.name = dictionary["name"]
        self.code = dictionary["code"]
        self.short_name = dictionary["shortName"]
        self.unit = dictionary["unit"]

    def __repr__(self):
        return "OasiParameter ({})".format(self.short_name)

    def __str__(self):
        return "OasiParameter:" \
               "\n\t   name: {}" \
               "\n\t   code: {}" \
               "\n\t   unit: {}".format(self.name, self.code, self.unit)


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

        if "parameters" not in parsed_settings:
            raise RuntimeError("Could not load 'parameters' key from parsed settings.")
        self.parameter_list = parsed_settings["parameters"]

    @staticmethod
    def __settings_hook(dictionary: dict):
        if "coordinates" in dictionary:
            return Location(dictionary)
        elif "shortName" in dictionary:
            return Parameter(dictionary)
        else:
            return dictionary
