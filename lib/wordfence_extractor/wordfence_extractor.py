from typing import List, Dict

from lib import fetch_vulnerabilities, match_vulnerabilities
from models.AppConfig import AppConfig
from models.ExtractorConfig import ExtractorConfig
from models.Vulnerability import Vulnerability


def wordfence_extractor(
        wordfence_url: str,
        global_config: ExtractorConfig,
        application_list: List[AppConfig]
) -> Dict[str, List[Vulnerability]]:
    api_data = fetch_vulnerabilities(wordfence_url)
    return match_vulnerabilities(
        api_data,
        application_list,
        global_config
    )
