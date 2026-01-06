from typing import List, Optional


class AppConfig:
    app_name: str
    dependencies: List[str]
    notify_url: Optional[str]
    notify_token: Optional[str]

    def __init__(self, app_name: str, dependencies: List[str], notify_url: str, notify_token: str) -> None:
        self.app_name = app_name
        self.dependencies = dependencies
        self.notify_url = notify_url
        self.notify_token = notify_token
