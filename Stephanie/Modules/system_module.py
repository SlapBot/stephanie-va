import datetime as dt
from Stephanie.Modules.base_module import BaseModule


class SystemModule(BaseModule):
    def __init__(self, *args):
        super(SystemModule, self).__init__(*args)
        self.name = self.get_configuration(section="USER", key="name")
        self.gender = self.get_configuration(section="USER", key="gender")

    def default(self):
        return "Repeat back your command!."

    def meaning_of_life(self):
        return "42 is the meaning of life."

    def time_right_now(self):
        t = dt.datetime.now()
        return self.time_teller(t)

    def date_today(self):
        t = dt.datetime.now()
        return self.date_teller(t)

    def wake_up(self):
        t = dt.datetime.now()
        if self.gender:
            gender = self.gender.lower()
            if gender == "male":
                return "%s, sir!" % self.phase_of_the_day(t)
            elif gender == "female":
                return "%s, sir!" % self.phase_of_the_day(t)
            else:
                return "%s, sir!" % self.phase_of_the_day(t)
        elif self.name:
            return "%s, %s!" % (self.phase_of_the_day(t), self.name)
        else:
            return "%s!" % self.phase_of_the_day(t)
    # Example to access assistant instance
    # def wake_up(self):
    #     self.assistant.say("What time is it again?")
    #     text = self.assistant.listen().decipher()
    #     return "Good %s, sir!" % text

    def go_to_sleep(self):
        self.assistant.events.add("sleep").trigger("sleep")
        return "Sleep for the weak!"

    def quit(self):
        self.assistant.events.add("quit").trigger("quit")
        return "I will come back stronger!"

    def tell_system_status(self):
        import psutil
        import platform
        import datetime

        os, name, version, _, _, _ = platform.uname()
        version = version.split('-')[0]
        cores = psutil.cpu_count()
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory()[2]
        disk_percent = psutil.disk_usage('/')[3]
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        running_since = boot_time.strftime("%A %d. %B %Y")
        response = "I am currently running on %s version %s.  " % (os, version)
        response += "This system is named %s and has %s CPU cores.  " % (name, cores)
        response += "Current disk_percent is %s percent.  " % disk_percent
        response += "Current CPU utilization is %s percent.  " % cpu_percent
        response += "Current memory utilization is %s percent. " % memory_percent
        response += "it's running since %s." % running_since
        return response

    @staticmethod
    def time_teller(time):
        # t = time.strftime('%I %M %H')
        # phase = time.strftime("%p")
        t = time.strftime("%I:%M:%p")

        d = {0: "oh",
             1: "one",
             2: "two",
             3: "three",
             4: "four",
             5: "five",
             6: "six",
             7: "seven",
             8: "eight",
             9: "nine",
             10: "ten",
             11: "eleven",
             12: "twelve",
             13: "thirteen",
             14: "fourteen",
             15: "fifteen",
             16: "sixteen",
             17: "seventeen",
             18: "eighteen",
             19: "nineteen",
             20: "twenty",
             30: "thirty",
             40: "forty",
             50: "fifty",
             60: "sixty"}

        time_array = t.split(":")
        hour, minute, phase = int(time_array[0]), int(time_array[1]), time_array[2]
        # hour = d[hour]
        # minute = d[minute]

        return "The time is %s %s %s" % (hour, minute, phase)
        #
        # hour = d[int(t[0:2])] if t[0:2] != "00" else d[12]
        # # suffix = 'a.m.' if d[int(t[7:9])] == hour else 'p.m.'
        # suffix = phase
        #
        # if t[3] == "0":
        #     if t[4] == "0":
        #         minute = ""
        #     else:
        #         minute = d[0] + " " + d[int(t[4])]
        # else:
        #     minute = d[int(t[3]) * 10] + '-' + d[int(t[4])]
        # return 'The time is %s %s %s.' % (hour, minute, suffix)

    @staticmethod
    def date_teller(date):
        return date.strftime("It's %A, %d %B %Y today!")

    @staticmethod
    def phase_of_the_day(time):
        hour = time.hour
        if hour < 12:
            return 'Good Morning'
        elif 12 <= hour < 18:
            return 'Good Afternoon'
        if hour > 6:
            return 'Good Evening'
