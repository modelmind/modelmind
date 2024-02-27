from modelmind.models.analytics.base import BaseAnalytics
from modelmind.models.analytics.schemas import Analytics


def combine_analytics_to_schema(analytics: list[BaseAnalytics]) -> list[Analytics]:
    return [analytic.to_schema() for analytic in analytics]
