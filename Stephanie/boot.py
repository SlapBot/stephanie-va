import speech_recognition as sr
from Stephanie.activity import Activity
from Stephanie.virtual_assistant import VirtualAssistant
from Stephanie.EventDispatcher.event_dispatcher import EventDispatcher
from Stephanie.TextManager.text_manager import TextManager
from Stephanie.configurer import config
from Stephanie.updater import Updater


class Boot:
    def __init__(self):
        self.status = False
        self.active = False
        self.events = EventDispatcher()
        self.speaker = TextManager()
        self.c = config
        self.updater = Updater(self.speaker)

    def initiate(self):
        print("Stephanie is on and loading, wait for the beep sound to give your command.")
        if self.c.config.getboolean("APPLICATION", "update_check"):
            self.updater.check_for_update()
        self.status = True
        if self.c.config.getboolean("SYSTEM", "wake_up_engine"):
            self.status = False
            self.active = False
        if self.c.config.getboolean("SYSTEM", "always_on_engine"):
            self.status = False
            self.active = False
        r = sr.Recognizer()
        act = Activity(sr, r, self.events)
        assistant = VirtualAssistant(sr, r, self.events)
        if self.c.config.getboolean("SYSTEM", "wake_up_engine"):
            while not self.active:
                with sr.Microphone() as source:
                    self.active = act.check(source)
                    self.status = self.active
                    self.events.sleep_status = not self.status
                    if self.active:
                        self.speaker.speak("How may I help you?")
                        while self.status:
                            with sr.Microphone() as source:
                                assistant.main(source)
                                if self.events.active_status:
                                    self.status = False
                                    self.active = True
                                elif self.events.sleep_status:
                                    self.status = False
                                    self.active = False
        elif self.c.config.getboolean("SYSTEM", "always_on_engine"):
            while not self.active:
                with sr.Microphone() as source:
                    self.active = act.check_always_on(source)
                    self.status = self.active
                    if self.active:
                        while self.status:
                            with sr.Microphone() as source:
                                assistant.main(source)
                                self.status = False
                                self.active = False
                                if self.events.active_status:
                                    self.status = False
                                    self.active = True
        else:
            self.speaker.speak("How may I help you?")
            while self.status:
                with sr.Microphone() as source:
                    assistant.main(source)
                    if self.events.active_status:
                        self.status = False
