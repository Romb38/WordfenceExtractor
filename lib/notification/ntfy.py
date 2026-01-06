from collections import defaultdict
from typing import List, Dict

import requests

from lib.configuration import logger
from models import Vulnerability


def vuln_ref_to_markdown(vuln : Vulnerability):
    """
    Return a Markdown link for the vulnerability.
    Priority:
    1. Reference URL if provided
    2. Generated NVD URL from CVE

    :param vuln: Vulnerability concerned
    :return: Url String
    """
    url = vuln.url
    cve = vuln.severity

    if url:
        label = cve if cve and cve != "None" else "reference"
        return f"[{label}]({url})"

    if cve and cve != "None":
        cve = cve.strip().upper()
        if cve.startswith("CVE-"):
            return f"[{cve}](https://nvd.nist.gov/vuln/detail/{cve})"

    return ""


def build_vuln_message(vulns : List[Vulnerability]):
    """
    Build a clean Markdown message for ntfy

    :param vulns: Vulnerabilities found
    :return: Markdown string of vulnerability
    """
    grouped : Dict[str, List[Vulnerability]] = defaultdict(list)
    for v in vulns:
        grouped[v.severity].append(v)

    severity_icons = {
        "Critical": "🚨",
        "High": "🔴",
        "Medium": "🟠",
        "Low": "🟡"
    }

    lines = [
        f"**{len(vulns)} vulnerabilities detected**",
        ""
    ]

    for severity in sorted(grouped.keys()):
        items = grouped[severity]
        icon = severity_icons.get(severity, "⚪")

        lines.append(f"{icon} **{severity} ({len(items)})**")

        for v in items:
            status = "✅ Patched" if v.patched else "❌ Not patched"
            ref_link = vuln_ref_to_markdown(v)

            line = f"- **{v.plugin_name}** — {v.title} ({status})"
            if ref_link:
                line += f" — {ref_link}"

            lines.append(line)

        lines.append("")

    return "\n".join(lines)


def notify_site(
        app_name : str,
        vulns : List[Vulnerability],
        notify_url : str,
        token : str
):
    """
    Send a notification to user using Ntfy API with found vulnerabilities

    :param app_name: Application concerned
    :param vulns: List of vulnerabilities found
    :param notify_url: Ntfy API URL
    :param token: Token (can be None)
    """

    message = build_vuln_message(vulns)

    if not notify_url:
        logger.debug(f"{app_name} : No NTFY URL given")
        return

    if not message:
        logger.info(f"{app_name} : No vulnerability to send")
        return

    headers = {
        "Title": f"{app_name} security report",
        "Markdown": "yes"
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        response = requests.post(notify_url, headers=headers, data=message.encode("utf-8"))
        if response.status_code >= 400:
            logger.error(f"{app_name} : NTFY failed with status {response.status_code} - {response.text}")
        else:
            logger.info(f"{app_name} : Notification sent successfully")
    except Exception as e:
        logger.error(f"{app_name} : Error sending NTFY notification - {e}")