from lib import logger, fetch_vulnerabilities, match_vulnerabilities, notify_site, load_config, get_sites, \
    get_global_filters
from lib.ntfy import build_vuln_message
from lib.wordfence_extractor.wordfence_extractor import wordfence_extractor

app_types = ["wordpress"]


def main():
    config_file = load_config("config.ini")
    config = get_global_filters(config_file)
    logger.info("Configuration loaded")
    logger.info(f"PATCHED={config.patch}, MIN_DANGER={config.min_danger}, SINCE={config.since}")

    for app_type in app_types:
        app_type_url = config_file["CONFIG"][app_type.upper()]
        apps = get_sites(config_file, app_type)
        results = wordfence_extractor(app_type_url, config, apps)

        for app_name, vulns in results.items():
            logger.info(f"{app_name} ({app_type}): {len(vulns)} vulnerabilities found")
            app = [app_item for app_item in apps if app_item.app_name == app_name][0]

            notify_site(
                app_name,
                build_vuln_message(vulns),
                app.notify_url,
                app.notify_token,
            )


if __name__ == "__main__":
    main()
