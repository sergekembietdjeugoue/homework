import requests
import datetime
import json
import os

# File to store query results
CACHE_FILE = "weather_cache.json"

# Example coordinates (London)
DEFAULT_LAT = 51.5074
DEFAULT_LON = -0.1278

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=4)

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

def fetch_weather(lat, lon, date):
    url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        f"&daily=precipitation_sum&timezone=Europe%2FLondon"
        f"&start_date={date}&end_date={date}"
    )
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "daily" in data and "precipitation_sum" in data["daily"]:
            return data["daily"]["precipitation_sum"][0]
        else:
            return None
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def interpret_precipitation(value):
    if value is None or value < 0:
        return "I don't know"
    elif value == 0.0:
        return "It will not rain"
    else:
        return f"It will rain (precipitation: {value} mm)"

def main():
    cache = load_cache()

    date = get_date_from_user()
    key = f"{DEFAULT_LAT},{DEFAULT_LON},{date}"

    if key in cache:
        print("(from cache)")
        precipitation = cache[key]
    else:
        precipitation = fetch_weather(DEFAULT_LAT, DEFAULT_LON, date)
        cache[key] = precipitation
        save_cache(cache)

    print(interpret_precipitation(precipitation))

if __name__ == "__main__":
    main()
