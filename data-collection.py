import data_service
import utils
import json
from data_collection_config import COUNTRY_PREFIXES, CONFIG
from time import sleep


def load_database():
    return json.loads(utils.read_from_file("data.json"))

database_content = load_database()
config = [c for c in CONFIG if c["key"] not in database_content]

for params in config:
    print(f"Loading data for {params['name']} ...")

    lines = data_service.fetch_lines_at_station(params["station_id"], COUNTRY_PREFIXES[params["country"]])

    database_content = load_database()
    database_content[params["key"]] = {
        "params": params,
        "lines": lines
    }
    utils.write_to_file("data.json", json.dumps(database_content))

    print(f"Loaded {len(lines)} lines for {params['name']}.")
    
    if params != config[-1]:
        print("Now sleeping for one minute ...")
        sleep(60)
        print()

print("Done.")