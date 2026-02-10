from typing import Optional, Dict
import requests
from .base import Notifier


class DiscordNotifier(Notifier):
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def notify(
        self,
        title: str,
        message: str,
        metadata: Optional[Dict] = None
    ):
        embed = {
            "title": title,
            "description": message,
            "color": 3447003,
        }

        if metadata:
            embed["fields"] = [
                {
                    "name": key.replace("_", " ").title(),
                    "value": str(value),
                    "inline": True
                }
                for key, value in metadata.items()
            ]

        payload = {"embeds": [embed]}

        response = requests.post(self.webhook_url, json=payload)
        response.raise_for_status()