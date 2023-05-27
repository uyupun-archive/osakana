from zoneinfo import ZoneInfo

from settings import Settings


def get_timezone(settings: Settings = Settings.get_settings()) -> ZoneInfo:
    timezone = settings.TIMEZONE
    return ZoneInfo(timezone)
