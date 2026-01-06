from typing import List, Dict

from .vulnerability_extractor import match_vulnerabilities, fetch_vulnerabilities
from models import ExtractorConfig, AppConfig, Vulnerability


def wordfence_extractor(
        wordfence_url: str,
        global_config: ExtractorConfig,
        application_list: List[AppConfig]
) -> Dict[str, List[Vulnerability]]:
    """
    Extract vulnerabilities from a wordfence app

    :param wordfence_url: Official wordfence url defined in config
    :param global_config: Global config
    :param application_list: List of applications specified in config
    :return: Dict[app_name, vulnerabilities]
    """
    api_data = fetch_vulnerabilities(wordfence_url)
    return match_vulnerabilities(
        api_data,
        application_list,
        global_config
    )
