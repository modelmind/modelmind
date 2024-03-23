from modelmind.clients.discord.webhook import DiscordWebhookClient
from modelmind.config import settings


def get_discord_notifications_webhook_client() -> DiscordWebhookClient:
    return DiscordWebhookClient(
        base_url=settings.discord.webhook_base_url,
        webhook_id=settings.discord.notifications_webhook_id,
        timeout=8000,
    )
