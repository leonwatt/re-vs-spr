import requests
import utils

def fetch_departures(station_id):
    url = f"https://v5.db.transport.rest/stops/{station_id}/departures?subway=false&tram=false&bus=false&duration=120&when=2022-04-20T10:00:00"
    print(f"GET {url}")
    response = requests.get(url).json()
    return [{
        "tripId": dep["tripId"],
        "direction": dep["direction"],
        "line_name": dep["line"]["name"],
        "line_id": dep["line"]["id"],
        "admin": dep["line"]["adminCode"],
        "type": dep["line"]["product"],
        "type_name": dep["line"]["productName"] if "productName" in dep["line"] else "",
        "operator_name": dep["line"]["operator"]["name"],
        "operator_id": dep["line"]["operator"]["id"]
    } for dep in response]

def fetch_stops(dep, country_prefix = None):
    url = f"https://v5.db.transport.rest/trips/{dep['tripId']}?lineName={dep['line_name']}"
    print(f"GET {url}")
    response = requests.get(url).json()
    return [{
        "name": st["stop"]["name"],
        "id": st["stop"]["id"],
        "location": (st["stop"]["location"]["latitude"], st["stop"]["location"]["longitude"]),
    } for st in response["stopovers"] if country_prefix == None or st["stop"]["id"].startswith(country_prefix)]


def fetch_lines_at_station(station_id, country_prefix = None):
    deps = fetch_departures(station_id)
    lines = utils.filter_duplicates(deps, lambda dep: f"{dep['direction']}-{dep['line_id']}-{dep['admin']}")
    for l in lines:
        l["stops"] = fetch_stops(l, country_prefix)
    return lines
