import subprocess

from lib import logger


def notify_site(site, vulns, notify_url, token):
    """
    Send a notification to user using Ntfy API with found vulnerabilities
    :param site: Website concerned
    :param vulns: Vulnerabilities founds
    :param notify_url: Ntfy API URL
    :param token: Token (can be None)
    :return: None
    """
    if not notify_url:
        logger.debug(f"{site} : No NTFY URL given")
        return

    if not vulns:
        logger.info(f"{site} : No vulnerability to send")
        return

    logger.info(f"{site} : send {len(vulns)} notification(s)")

    message = f"{site} – {len(vulns)} detected vulnerabilities \n\n"
    for v in vulns:
        status = "PATCHED" if v["patched"] else "NOT PATCHED"
        message += f"- [{v['severity']}] {v['plugin']} ({status}) – {v['title']} {v['cve']}\n"

    cmd = [
        "curl", "-X", "POST", notify_url,
        "-H", "Content-Type: application/json",
        "-H", f"Authorization: Bearer {token}" if token else "",
        "-d", f'{{"message": "{message.replace(chr(10), "\\n")}"}}'
    ]
    cmd = [c for c in cmd if c]

    subprocess.run(cmd, capture_output=True)
