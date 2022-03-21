import requests
from decouple import config

appid = config("OPEN_WEATHER_KEY")


class Forecast:
    def __init__(self, city):
        self.city = city
        self.city_id = self.take_city_id()
        self.data = self.take_data() if self.city_id is not None else None

    def take_city_id(self):
        res = requests.get(
            "http://api.openweathermap.org/data/2.5/find",
            params={"q": self.city, "type": "like", "units": "metric", "APPID": appid},
        )
        data = res.json()

        try:
            city_id = data["list"][0]["id"]
        except IndexError:
            print("Exception (find):", "IndexError")
            city_id = None

        print("city_id=", city_id)
        return city_id

    def take_data(self):
        try:
            res = requests.get(
                "http://api.openweathermap.org/data/2.5/forecast",
                params={
                    "id": self.city_id,
                    "units": "metric",
                    "lang": "ru",
                    "APPID": appid,
                },
            )
            data = res.json()
            return data
        except Exception as e:
            print("Exception (forecast):", e)

    def forecast_for_several_days(self):
        forecast_weather = []
        for i in self.data["list"]:
            if i["dt_txt"].endswith("12:00:00"):
                weather = {
                    "date": i["dt_txt"].split()[0],
                    "temp": "{0:+3.0f}".format(i["main"]["temp"]),
                    "description": i["weather"][0]["description"],
                }
                forecast_weather.append(weather)

        return forecast_weather

    def forecast_for_specific_day(self, date):
        forecast_weather = []
        for i in self.data["list"]:
            if i["dt_txt"].startswith(date):
                weather = {
                    "time": i["dt_txt"].split()[1],
                    "temp": "{0:+3.0f}".format(i["main"]["temp"]),
                    "description": i["weather"][0]["description"],
                }
                forecast_weather.append(weather)

        if forecast_weather:
            return forecast_weather
        else:
            return None
