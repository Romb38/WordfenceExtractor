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
        logger.debug(f"{site} : aucune URL de notification définie")
        return

    if not vulns:
        logger.info(f"{site} : aucune vulnérabilité à notifier")
        return

    logger.info(f"{site} : envoi de {len(vulns)} notification(s)")

    message = f"{site} – {len(vulns)} vulnérabilité(s) détectée(s)\n\n"
    for v in vulns:
        status = "PATCHÉE" if v["patched"] else "NON PATCHÉE"
        message += f"- [{v['severity']}] {v['plugin']} ({status}) – {v['title']} {v['cve']}\n"

    cmd = [
        "curl", "-X", "POST", notify_url,
        "-H", "Content-Type: application/json",
        "-H", f"Authorization: Bearer {token}" if token else "",
        "-d", f'{{"message": "{message.replace(chr(10), "\\n")}"}}'
    ]
    cmd = [c for c in cmd if c]

    subprocess.run(cmd, capture_output=True)