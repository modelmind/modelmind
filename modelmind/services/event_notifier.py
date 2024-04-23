from modelmind.clients.discord.schemas import Embed, Field, WebhookBody
from modelmind.clients.discord.webhook import DiscordWebhookClient
from modelmind.db.schemas.profiles import Biographics
from modelmind.models.analytics.schemas import Analytics


class EventNotifier:
    def __init__(self, discord_notifications_webhook_client: DiscordWebhookClient) -> None:
        self.discord_notifications_client = discord_notifications_webhook_client

    def format_analytics_to_message(
        self, questionnaire_name: str, analytics: list[Analytics], biographics: Biographics
    ) -> WebhookBody:
        embeds: list[Embed] = []

        def format_analytics_item(item: Analytics.ScoreItem) -> str:
            return f"**{item.name}**: Value: **{item.value}**, Percentage: **{item.percentage:.2f}**%"

        def format_fields(analytics: Analytics) -> list[Field]:
            return [
                {
                    "name": key,
                    "value": str(value),
                    "inline": True,
                }
                for key, value in analytics.extra.items()
                if isinstance(value, (int, float, str))
            ]

        def format_content(biographics: Biographics) -> str:
            mbti_type = biographics.get("personality", {}).get("mbti", {}).get("type", "Unknown")  # type: ignore
            mbti_confidence = biographics.get("personality", {}).get("mbti", {}).get("confidence", None)  # type: ignore
            return (
                f"**{mbti_type}** ({mbti_confidence}) - {biographics.get('birth_year')} - {biographics.get('gender')}"
            )

        descriptions = []
        fields: list[Field] = []

        for analysis in analytics:
            sorted_items = sorted(analysis.items, key=lambda x: x.value, reverse=True)
            descriptions.append("\n".join(format_analytics_item(item) for item in sorted_items))
            fields.extend(format_fields(analysis))

        embeds.append(
            {
                "title": format_content(biographics),
                "description": "\n\n".join(descriptions),
                "fields": fields,
                "color": 3447003,
            }
        )

        return {"username": questionnaire_name, "embeds": embeds}

    async def new_result(self, questionnaire_name: str, analytics: list[Analytics], biographics: Biographics) -> None:
        body = self.format_analytics_to_message(questionnaire_name, analytics, biographics)
        await self.discord_notifications_client.send_embed_message(body)
