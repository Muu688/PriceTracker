from typing import List
from .base import Notifier


class NotificationService:
    def __init__(self, notifiers: List[Notifier]):
        self.notifiers = notifiers

    def notify_all(self, title: str, message: str, metadata: dict | None = None):
        for notifier in self.notifiers:
            notifier.notify(title, message, metadata)