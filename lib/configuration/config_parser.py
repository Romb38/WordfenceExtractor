import configparser
from datetime import datetime, timedelta
import json
from typing import List

from models import AppConfig, ExtractorConfig, DangerLevel


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


def get_sites(config, scan_type):
    """
    Retrieves the sites configured in the config file
    :param config: Dictionary of configuration
    :param scan_type: Scan asked
    :return: Dictionary of sites
    """
    sites : List[AppConfig] = []

    for section in config.sections():
        if section == "CONFIG":
            continue

        if not (config[section].get("scan_type") and config[section]["scan_type"].lower() == scan_type.lower()):
            continue

        sites.append(AppConfig(
            app_name=section,
            dependencies=[p.strip() for p in json.loads(config[section].get("dependencies", "None").replace("\n", "")) if
                         p.strip()],
            notify_url=config[section].get("notify_url", "").strip(),
            notify_token=config[section].get("notify_token", "").strip(),
        ))

    return sites


def get_global_filters(config):
    """
    Retrieves the global filters configured in the config file
    :param config: Dictionary of configuration
    :return: Global filters object
    """
    patched = config["CONFIG"].getboolean("PATCHED", fallback=True)
    min_danger = config["CONFIG"].get("MIN_DANGER", "Low")

    since_raw = config["CONFIG"].get("SINCE", "").strip()
    since_date = parse_since(since_raw) if since_raw else None

    return ExtractorConfig(
        patch=patched,
        min_danger=DangerLevel(min_danger),
        since=since_date
    )
