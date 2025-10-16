import requests
import datetime
import json
import os

CACHE_FILE = "weather_cache.json"
DEFAULT_LAT = 51.5074
DEFAULT_LON = -0.1278

class WeatherForecast:
    def __init__(self, cache_file=CACHE_FILE, lat=DEFAULT_LAT, lon=DEFAULT_LON):
        self.cache_file = cache_file
        self.lat = lat
        self.lon = lon
        self._cache = self._load_cache()

    def _load_cache(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def _save_cache(self):
        with open(self.cache_file, "w") as f:
            json.dump(self._cache, f, indent=4)

    def __setitem__(self, date, value):
        key = f"{self.lat},{self.lon},{date}"
        self._cache[key] = value
        self._save_cache()

    def __getitem__(self, date):
        key = f"{self.lat},{self.lon},{date}"
        if key in self._cache:
            return self._cache[key]
        precipitation = self._fetch_weather(date)
        self[key] = precipitation
        return precipitation

    def __iter__(self):
        for key in self._cache.keys():
            parts = key.split(",")
            if len(parts) == 3:
                yield parts[2]  # date only

    def items(self):
        for key, value in self._cache.items():
            parts = key.split(",")
            if len(parts) == 3:
                yield (parts[2], value)

    def _fetch_weather(self, date):
        url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}"
            f"&daily=precipitation_sum&timezone=Europe%2FLondon"
            f"&start_date={date}&end_date={date}"
        )
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if "daily" in data and "precipitation_sum" in data["daily"]:
                return data["daily"]["precipitation_sum"][0]
            return None
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

def get_date_from_user():
    user_input = input("Enter a date (YYYY-mm-dd) [default: tomorrow]: ").strip()
    if not user_input:
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        return tomorrow.strftime("%Y-%m-%d")
    try:
        datetime.datetime.strptime(user_input, "%Y-%m-%d")
        return user_input
    except ValueError:
        print("Invalid date format. Please use YYYY-mm-dd.")
        return get_date_from_user()

def interpret_precipitation(value):
    if value is None or value < 0:
        return "I don't know"
    elif value == 0.0:
        return "It will not rain"
    else:
        return f"It will rain (precipitation: {value} mm)"

def main():
    weather_forecast = WeatherForecast()
    date = get_date_from_user()
    precipitation = weather_forecast[date]
    print(interpret_precipitation(precipitation))

    print("\nSaved forecasts:")
    for d, w in weather_forecast.items():
        print(d, "->", interpret_precipitation(w))

if __name__ == "__main__":
    main()
