from typing import List, Dict

import requests

from models import ExtractorConfig, AppConfig, Vulnerability, DangerLevel


def osv_extractor(
        osv_url: str,
        global_config: ExtractorConfig,
        application_list: List[AppConfig]
) -> Dict[str, List[Vulnerability]]:
    """
    Extract vulnerabilities from a wordfence app

    :param osv_url: Official OSV url defined in config
    :param global_config: Global config
    :param application_list: List of applications specified in config
    :return: Dict[app_name, vulnerabilities]
    """
    results = {}

    # Map DangerLevel to OSV severity mapping
    danger_to_osv = {
        DangerLevel.Low: "LOW",
        DangerLevel.Medium: "MEDIUM",
        DangerLevel.High: "HIGH",
        DangerLevel.Critical: "CRITICAL"
    }
    min_severity_value = list(danger_to_osv.keys()).index(global_config.min_danger)

    for app_config in application_list:
        app_vulns = []

        for dep in app_config.dependencies:
            # Construire le corps de la Star OSV
            payload = {
                "package": {
                    "name": dep,
                }
            }
            if global_config.since is not None:
                payload["since"] = global_config.since.isoformat()

            try:
                response = requests.post(f"{osv_url}", json=payload)
                response.raise_for_status()
                data = response.json()

                for vuln in data.get("vulns", []):
                    # Filtrer par sévérité
                    osv_severity = vuln.get("severity", [{}])[0].get("score", "UNKNOWN")
                    if osv_severity not in danger_to_osv.values():
                        continue
                    severity_level = list(danger_to_osv.values()).index(osv_severity)
                    if severity_level < min_severity_value:
                        continue

                    # Vérifier si patché
                    patched = False
                    for affected in vuln.get("affected", []):
                        for r in affected.get("ranges", []):
                            if r.get("type") == "GIT":
                                patched = True
                                break
                        if patched:
                            break

                    if not global_config.patch and patched:
                        continue

                    # Extraire CVE
                    cve = None
                    for alias in vuln.get("aliases", []):
                        if alias.startswith("CVE-"):
                            cve = alias
                            break

                    # Créer l'objet Vulnerability
                    vuln_obj = Vulnerability(
                        vuln_id=vuln["id"],
                        title=vuln.get("summary", ""),
                        plugin_name=dep,
                        severity=osv_severity,
                        patched=patched,
                        cve=cve,
                        url=vuln.get("database_specific", {}).get("url", None)
                    )
                    app_vulns.append(vuln_obj)

            except Exception as e:
                print(f"Error fetching OSV data for {dep}: {e}")
                continue

        results[app_config.app_name] = app_vulns

    return results
