from modelmind.config import settings
from modelmind.services.discord.webhook import DiscordWebhookClient


def get_discord_notifications_webhook_client() -> DiscordWebhookClient:
    return DiscordWebhookClient(
        base_url=settings.discord.webhook_base_url,
        webhook_id=settings.discord.notifications_webhook_id,
        timeout=8000,
    )
