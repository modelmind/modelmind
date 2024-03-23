from fastapi import Depends

from modelmind.api.public.dependencies.clients.discord import get_discord_notifications_webhook_client
from modelmind.clients.discord.webhook import DiscordWebhookClient
from modelmind.services.event_notifier import EventNotifier


def get_event_notifier(
    discord_notifications_webhook_client: DiscordWebhookClient = Depends(get_discord_notifications_webhook_client),
) -> EventNotifier:
    return EventNotifier(discord_notifications_webhook_client=discord_notifications_webhook_client)
