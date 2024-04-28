from typing import Optional

from modelmind.clients.discord.schemas import Embed, Field, WebhookBody
from modelmind.clients.discord.webhook import DiscordWebhookClient
from modelmind.db.schemas.profiles import Biographics
from modelmind.models.analytics.schemas import Analytics


class EventNotifier:
    def __init__(self, discord_notifications_webhook_client: DiscordWebhookClient) -> None:
        self.discord_notifications_client = discord_notifications_webhook_client

    @staticmethod
    def get_persony_color(predicted_dominants: str, target_dominants: Optional[str] = None) -> int:
        # related to persony test
        # TODO: find a better way to separate this business logic
        if predicted_dominants == target_dominants:
            return 0x00FF00
        elif not target_dominants:
            return 0x34B7EB
        else:
            return 0xFF0000

    def format_analytics_to_message(
        self, questionnaire_name: str, label: str | None, analytics: list[Analytics], biographics: Biographics
    ) -> WebhookBody:
        embeds: list[Embed] = []

        def format_analytics_item(item: Analytics.ScoreItem) -> str:
            return f"**{item.name}**: Value: **{item.value}**, Percentage: **{item.percentage:.2f}**%"

        def format_extra_fields(analytics: Analytics) -> list[Field]:
            return [
                {
                    "name": key,
                    "value": str(value),
                    "inline": True,
                }
                for key, value in analytics.extra.items()
                if isinstance(value, (int, float, str))
            ]

        def format_biographics(biographics: Biographics) -> str:
            mbti_type = biographics.get("personality", {}).get("mbti", {}).get("type", "Unknown")  # type: ignore
            mbti_confidence = biographics.get("personality", {}).get("mbti", {}).get("confidence", None)  # type: ignore
            return (
                f"**{mbti_type}** ({mbti_confidence}) - {biographics.get('birth_year')} - {biographics.get('gender')}"
            )

        descriptions = []
        fields: list[Field] = []

        for analysis in analytics:
            sorted_items = sorted(analysis.items, key=lambda x: x.percentage or x.value, reverse=True)
            descriptions.append("\n".join(format_analytics_item(item) for item in sorted_items))

        fields.append({"name": "Biographics", "value": format_biographics(biographics), "inline": False})

        # TODO: remove this business logic
        target_dominants = biographics.get("personality", {}).get("mbti", {}).get("type", None)  # type: ignore

        embeds.append(
            {
                "title": label or "N/A",
                "description": "\n\n".join(descriptions),
                "fields": fields,
                "color": self.get_persony_color(label or "", target_dominants),
            }
        )

        return {"username": questionnaire_name, "embeds": embeds}

    async def new_result(
        self, questionnaire_name: str, label: str | None, analytics: list[Analytics], biographics: Biographics
    ) -> None:
        body = self.format_analytics_to_message(questionnaire_name, label, analytics, biographics)
        await self.discord_notifications_client.send_embed_message(body)
