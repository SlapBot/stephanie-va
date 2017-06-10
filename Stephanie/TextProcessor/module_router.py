import re
import importlib
from Stephanie.TextProcessor.audio_text_manager import AudioTextManager
from Stephanie.configurer import config


# noinspection PyPep8Naming
class ModuleRouter:
    def __init__(self, events):
        self.audio_text_manager = AudioTextManager(events)
        self.virtual_assistant_name = "Stephanie"
        self.modules_directory_name = "Modules"
        self.module_path = ""
        self.moduleName = ""
        self.function_name = ""
        self.c = config

    def inject(self, module_info, raw_text, sub_words, key_words):
        moduleRawName = module_info[0]
        key_words_available = module_info[1]
        result_speech_text = self.process_module(moduleRawName).apply(key_words_available, raw_text,
                                                                      sub_words, key_words)
        return result_speech_text

    def process_module(self, moduleRawName):
        try:
            moduleNameInfo = moduleRawName.split("@")
            self.moduleName = moduleNameInfo[0]
            functionName = moduleNameInfo[1]
            self.function_name = self.convert_to_snake_case(functionName)
            module_name = self.convert_to_snake_case(self.moduleName)
            self.module_path = "{0}.{1}.{2}".format(self.virtual_assistant_name,
                                                    self.modules_directory_name,
                                                    module_name)
        except:
            raise Exception("module name wasn't configured as defined in the convention terms in the docs."
                            " fault is of that 3rd party module guy, or If I went drunk, and I never go drunk. "
                            "Read the developer guide properly to wire in the module.")
        return self

    def apply(self, key_words_available, raw_text, sub_words, key_words):
        try:
            my_module = importlib.import_module(self.module_path)
        except:
            raise Exception("Module you are trying to use isn't available, go the docs, to know "
                            "how to install it properly Read the developer guide thoroughly,"
                            " or if you're using 3rd party module,"
                            " contact him, but still you will contact me so it's fine, I will help you."
                            " Consider checking the support tab of main website if any extra help is needed.")
        try:
            className = getattr(my_module, self.moduleName)
            instance = className(key_words_available, raw_text, sub_words, key_words,
                                 self.audio_text_manager, self.c)
            result_speech_text = getattr(instance, self.function_name)()
            return result_speech_text
        except:
            raise Exception("No such class name exists or such method on that instance of class exists,"
                            " you shouldn't be getting this if you are good ol user and not a 3rd party"
                            " developer, for you mr.developer, check the support tab, to know how to fix it or just"
                            " read the guidelines thoroughly to learn how to create your own modules and wire them properly.")

    @staticmethod
    def convert_to_snake_case(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
