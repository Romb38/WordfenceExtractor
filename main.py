from lib import logger, fetch_vulnerabilities, match_vulnerabilities, notify_site, load_config, get_sites, \
    get_global_filters


def main():
    config = load_config("config.ini")

    api_url = config["CONFIG"]["API_URL"]
    sites = get_sites(config)
    patched, min_danger, since_date = get_global_filters(config)

    logger.info("Configuration loaded")
    logger.info(f"PATCHED={patched}, MIN_DANGER={min_danger}, SINCE={since_date}")

    api_data = fetch_vulnerabilities(api_url)
    results = match_vulnerabilities(api_data, sites, patched, min_danger, since_date)

    for site, vulns in results.items():
        logger.info(f"{site} : {len(vulns)} vulnerabilities found")
        notify_site(
            site,
            vulns,
            sites[site]["notify_url"],
            sites[site]["notify_token"]
        )


if __name__ == "__main__":
    main()
