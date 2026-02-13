from notifications.discord import DiscordNotifier
from notifications.service import NotificationService
import os

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

notifier = NotificationService([
    DiscordNotifier(WEBHOOK_URL)
])

def on_price_drop(product_name, old_price, new_price, product_url):
    notifier.notify_all(
        title="Price Drop Detected",
        message=f"**{product_name}** just got cheaper!",
        metadata={
            "Old price": f"${old_price}",
            "New price": f"${new_price}",
            "Savings": f"${old_price - new_price}",
            "Link": product_url
        }
    )