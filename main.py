from lib.configuration import get_sites, logger, get_global_filters, load_config
from lib.notification import notify_site
from lib.osv_extractor import osv_extractor
from lib.wordfence_extractor import wordfence_extractor

app_types = {
    "wordpress": wordfence_extractor,
    "osv": osv_extractor,
}

def main():
    # 1 - Load global config
    config_file = load_config("config.ini")
    config = get_global_filters(config_file)
    logger.info("Configuration loaded")
    logger.info(f"PATCHED={config.patch}, MIN_DANGER={config.min_danger}, SINCE={config.since}")

    # 2 - Go around every app_types to get vulnerability from
    for app_type, extractor_func in app_types.items():
        app_type_url = config_file["CONFIG"][app_type.upper()]
        apps = get_sites(config_file, app_type)
        results = extractor_func(app_type_url, config, apps)

        # 3 - Notify user for every website inside of this type
        for app_name, vulns in results.items():
            logger.info(f"{app_name} ({app_type}): {len(vulns)} vulnerabilities found")
            app = [app_item for app_item in apps if app_item.app_name == app_name][0]

            notify_site(
                app_name,
                vulns,
                app.notify_url,
                app.notify_token,
            )


if __name__ == "__main__":
    main()
