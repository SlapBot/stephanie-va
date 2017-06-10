import datetime
import pyowm
from Stephanie.Modules.base_module import BaseModule
from Stephanie.local_libs.numbers_format import NumberService


class WeatherReportModule(BaseModule):
    def __init__(self, *args):
        super(WeatherReportModule, self).__init__(*args)
        self.api_key = self.get_configuration("open_weather_map_api_key")
        if self.api_key:
            self.owm = pyowm.OWM(self.api_key)
        else:
            return False
        self.city = self.get_configuration(section="USER", key="city")
        self.num_service = NumberService()

    # def weather_information(self):
    #     self.assistant.say("What would you like to know about?")
    #     query = self.assistant.listen().decipher()

    def weather_report_weekly(self):
        temp_unit = 'celsius'
        # some problem with self.city variable
        forecast = self.owm.daily_forecast(self.city)
        fore = forecast.get_forecast()
        location = fore.get_location().get_name()
        weather_report = self.get_weather_report_weekly(forecast, location, temp_unit, report="weekly")
        return weather_report

    def weather_report_today(self):
        temp_unit = 'celsius'
        report = 'current'
        cw = self.owm.weather_at_place(self.city)
        loc = cw.get_location().get_name()
        weather = cw.get_weather()
        weather_report = self.get_weather_report(weather, loc, temp_unit, report)
        return weather_report

    def weather_report_tomorrow(self):
        temp_unit = 'celsius'
        report = 'tomorrow'
        forecast = self.owm.daily_forecast(self.city)
        fore = forecast.get_forecast()
        loc = fore.get_location().get_name()
        tomorrow = pyowm.timeutils.tomorrow()
        weather = forecast.get_weather_at(tomorrow)
        weather_report = self.get_weather_report(weather, loc, temp_unit, report)
        return weather_report

    def get_weather_report(self, weather, loc, temp_unit='celsius', report='current'):
        weather_report = 'Server Down.'
        wind = weather.get_wind()
        wind_speed = self.num_service.parseMagnitude(wind["speed"])
        humi = self.num_service.parseMagnitude(weather.get_humidity())
        if weather.get_clouds() > 0:
            clou = self.num_service.parseMagnitude(weather.get_clouds())
        else:
            clou = "zero"
        stat = weather.get_status()
        detstat = weather.get_detailed_status()

        if report == 'current':
            temp = weather.get_temperature(temp_unit)
            temp_max = self.num_service.parseMagnitude(temp['temp_max'])
            temp_min = self.num_service.parseMagnitude(temp['temp_min'])
            curr_temp = self.num_service.parseMagnitude(temp['temp'])
            weather_report = "Weather at " + loc + ". Today is " + stat + ". There is a chance of " \
                             + detstat + ". Now Temperature is " + curr_temp + " degree " \
                             + temp_unit + ". Humidity " + humi + " percent. Wind Speed " \
                             + wind_speed + ". with cloud cover " + clou + " percent."

        elif report == 'tomorrow':
            temp = weather.get_temperature(temp_unit)
            temp_morn = self.num_service.parseMagnitude(temp['morn'])
            temp_day = self.num_service.parseMagnitude(temp['day'])
            temp_night = self.num_service.parseMagnitude(temp['night'])
            weather_report = "Weather at " + loc + ". Tomorrow will be " + stat + ". There will be a chance of " \
                             + detstat + ". Temperature in the morning " + temp_morn + " degree " \
                             + temp_unit + ". Days Temperature will be " + temp_day + " degree " \
                             + temp_unit + ". and Temperature at night will be " + temp_night + " degree " \
                             + temp_unit + ". Humidity " + humi + " percent. Wind Speed " \
                             + wind_speed + ". with clouds cover " + clou + " percent."

        return weather_report

    def get_weather_report_weekly(self, forecast, loc, temp_unit='celsius', report='current'):
        weather_report = "Weather forecast for next week at " + loc + ". "
        rainy_days = len(forecast.when_rain())
        if rainy_days > 0:
            rainy_days_str = "Rainy Days are. "
            for d in range(rainy_days):
                rain_day = forecast.when_rain()[d].get_reference_time()
                date_str = self.format_time_stamp(rain_day)
                rainy_days_str += date_str + ". "

            weather_report += rainy_days_str
            date_str = ''

        most_rainy = forecast.most_rainy()
        if most_rainy:
            weather_report += "You will observe heavy rain on. "
            ref_time = most_rainy.get_reference_time()
            date_str = self.format_time_stamp(ref_time)
            weather_report += date_str + ". "
            date_str = ''

        sunny_days = len(forecast.when_sun())
        if sunny_days > 0:
            sunny_days_str = "Sunny Days are. "
            for d in range(sunny_days):
                sunny_day = forecast.when_sun()[d].get_reference_time()
                date_str = self.format_time_stamp(sunny_day)
                sunny_days_str += date_str + ". "

            weather_report += sunny_days_str
            date_str = ''

        most_hot = forecast.most_hot()
        if most_hot:
            weather_report += "You will feel heat on. "
            ref_time = most_hot.get_reference_time()
            date_str = self.format_time_stamp(ref_time)
            weather_report += date_str + ". "
            date_str = ''

        most_windy = forecast.most_windy()
        if most_windy:
            weather_report += "Most windy day will be. "
            ref_time = most_windy.get_reference_time()
            date_str = self.format_time_stamp(ref_time)
            weather_report += date_str + ". "
            date_str = ''

        most_humid = forecast.most_humid()
        if most_humid:
            weather_report += "Most humid day will be. "
            ref_time = most_humid.get_reference_time()
            date_str = self.format_time_stamp(ref_time)
            weather_report += date_str + ". "
            date_str = ''

        most_cold = forecast.most_cold()
        if most_cold:
            weather_report += "Coolest day will be. "
            ref_time = most_cold.get_reference_time()
            date_str = self.format_time_stamp(ref_time)
            weather_report += date_str + ". "
            date_str = ''

        return weather_report

    @staticmethod
    def format_time_stamp(unix_time):
        return datetime.datetime.fromtimestamp(unix_time).strftime("%B %d")
