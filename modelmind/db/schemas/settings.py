from typing import TypedDict


class StatisticsSchedulerSettings(TypedDict):
    persony: list[str]


class SchedulerSettings(TypedDict):
    statistics: StatisticsSchedulerSettings
