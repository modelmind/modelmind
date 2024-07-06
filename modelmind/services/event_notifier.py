from datetime import datetime
from typing import Optional

from modelmind.db.schemas.profiles import Biographics
from modelmind.db.schemas.questionnaires import DBQuestionnaire
from modelmind.db.schemas.statistics import AccuracyMetric, CountsMetric, PersonyStatistics
from modelmind.models.analytics.schemas import Analytics
from modelmind.services.discord.schemas import Embed, Field, WebhookBody
from modelmind.services.discord.webhook import DiscordWebhookClient


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

    def format_statistics_to_message(self, questionnaire_name: str, statistics: PersonyStatistics) -> WebhookBody:
        embeds: list[Embed] = []

        accuracy = statistics["accuracy"]
        counts = statistics["counts"]

        def format_accuracy(accuracy: AccuracyMetric) -> str:
            return (
                f"**Total Sample**: {accuracy['total']['total_predictions']}\n"
                f"**Acc. Percentage**: {accuracy['total']['percentage']:.2f}%\n\n"
                f"**Confidence >= 1**:\n"
                f"- Sample: {accuracy['confidence_ge_1']['total_predictions']}\n"
                f"- Percentage: {accuracy['confidence_ge_1']['percentage']:.2f}%\n\n"
                f"**Confidence >= 2**:\n"
                f"- Sample: {accuracy['confidence_ge_2']['total_predictions']}\n"
                f"- Percentage: {accuracy['confidence_ge_2']['percentage']:.2f}%\n\n"
                f"**Confidence >= 3**:\n"
                f"- Sample: {accuracy['confidence_ge_3']['total_predictions']}\n"
                f"- Percentage: {accuracy['confidence_ge_3']['percentage']:.2f}%\n\n"
                f"**Confidence >= 4**:\n"
                f"- Sample: {accuracy['confidence_ge_4']['total_predictions']}\n"
                f"- Percentage: {accuracy['confidence_ge_4']['percentage']:.2f}%"
            )

        def format_counts(counts: CountsMetric) -> str:
            return (
                f"**Total**: {counts['total']}\n"
                f"**With Label**: {counts['with_label']}\n"
                f"**Male**: {counts['male']}\n"
                f"**Female**: {counts['female']}\n"
                f"**Other**: {counts['other']}"
            )

        fields: list[Field] = [
            {"name": "Accuracy", "value": format_accuracy(accuracy), "inline": False},
            {"name": "Counts", "value": format_counts(counts), "inline": False},
        ]

        embeds.append(
            {
                "title": questionnaire_name,
                "description": f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "fields": fields,
                "color": 0x800080,
            }
        )

        return {"username": "Statistics Bot", "embeds": embeds, "content": "@everyone"}

    async def new_statistics(self, db_questionnaire: DBQuestionnaire, statistics: PersonyStatistics) -> None:
        body = self.format_statistics_to_message(db_questionnaire.name, statistics)
        await self.discord_notifications_client.send_embed_message(body)
