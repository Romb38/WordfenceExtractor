import datetime
from typing import Optional

from models.DangerLevel import DangerLevel


class ExtractorConfig:
    patch : bool
    min_danger: DangerLevel
    since: datetime.date

    def __init__(self, patch: bool, min_danger: DangerLevel, since: datetime.date) -> None:
        self.patch = patch
        self.min_danger = min_danger
        self.since = since