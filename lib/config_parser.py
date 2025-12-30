import configparser
from datetime import datetime, timedelta
import json


def load_config(path="config.ini"):
    """
    Loads the configuration file as a dictionary
    :param path: Path to the configuration file
    :return: Dictionary of configuration
    """
    config = configparser.ConfigParser()
    config.read(path)
    return config


def parse_since(value):
    """
    Transform the 7d or 14w in a timedelta object
    :param value: String in the format of <int>[d|w] with d=days and w=weeks
    :return: Timedelta object else None if no value where given
    """
    now = datetime.now()

    if value.endswith("d"):
        return now - timedelta(days=int(value[:-1]))
    if value.endswith("w"):
        return now - timedelta(weeks=int(value[:-1]))

    return None


def get_sites(config):
    """
    Retrieves the sites configured in the config file
    :param config: Dictionary of configuration
    :return: Dictionary of sites
    """
    sites = {}

    for section in config.sections():
        if section == "CONFIG":
            continue
        
        print(section)
        sites[section] = {
            "plugins": [p.strip() for p in json.loads(config[section].get("plugin_list", "None").replace("\n","")) if p.strip()],
            "notify_url": config[section].get("NOTIFY_URL", "").strip(),
            "notify_token": config[section].get("NOTIFY_TOKEN", "").strip()
        }

    return sites


def get_global_filters(config):
    """
    Retrieves the global filters configured in the config file
    :param config: Dictionary of configuration
    :return: Tuple with transformed configuration
    """
    patched = config["CONFIG"].getboolean("PATCHED", fallback=True)
    min_danger = config["CONFIG"].get("MIN_DANGER", "Low")

    since_raw = config["CONFIG"].get("SINCE", "").strip()
    since_date = parse_since(since_raw) if since_raw else None

    return patched, min_danger, since_date