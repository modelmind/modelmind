from modelmind.clients.httpx_client import HttpxClient


class DiscordWebhookClient(HttpxClient):
    def __init__(self, base_url: str, timeout: int = 8000) -> None:
        super().__init__(base_url, timeout)

    async def send_embed_message(self, username: str, title: str, description: str, color: int) -> None:
        payload = {
            "username": username,
            "embeds": [
                {
                    "title": title,
                    "description": description,
                    "color": color,
                }
            ],
        }
        await self.request("POST", "/", json=payload)
