from modelmind.clients.httpx_client import HttpxClient

from .schemas import WebhookBody


class DiscordWebhookClient(HttpxClient):
    def __init__(self, base_url: str, webhook_id: str, timeout: int = 8000) -> None:
        self.webhook_id = webhook_id
        print(f"DiscordWebhookClient: {webhook_id}")
        super().__init__(base_url, timeout)

    async def send_embed_message(self, webhook_body: WebhookBody) -> None:
        return await self.request("POST", f"{self.webhook_id}", json=webhook_body)
