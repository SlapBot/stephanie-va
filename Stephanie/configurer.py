import os
import configparser
import json


class Configurer:
    def __init__(self, filename="config.ini", modules_filename="modules.json"):
        print("initialised")
        self.abs_filename = self.get_abs_filename(filename)
        self.abs_mods_filename = self.get_abs_filename(modules_filename)
        self.config = configparser.ConfigParser()
        self.config.read(self.abs_filename)
        self.sections = self.config.sections()
        self.modules = self.retreive_modules(self.abs_mods_filename)

    @staticmethod
    def retreive_modules(abs_mods_filename):
        print("modules retreived.")
        try:
            with open(abs_mods_filename, "r") as file:
                modules = json.load(file)
                file.close()
        except Exception as e:
            raise Exception("Modules.json file has been not formatted correctly. check the support tab in case you're integrating some 3rd party module.") from e
        return modules

    def get_modules(self, filename=None):
        if filename:
            abs_mods_filename = self.get_abs_filename(filename)
            return self.retreive_modules(abs_mods_filename)
        return self.modules

    @staticmethod
    def get_abs_filename(filename):
        return os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            os.pardir, filename))


config = Configurer()
