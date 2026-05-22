RATE_LIMIT_KEYWORDS = (
    "429",
    "rate limit",
    "rate-limiting",
    "quota",
    "resource_exhausted",
    "exhausted your capacity",
    "too many requests",
)


def is_rate_limit_error(message: str) -> bool:
    text = message.lower()
    return any(keyword in text for keyword in RATE_LIMIT_KEYWORDS)


def human_duration(seconds: int) -> str:
    minutes, sec = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours} jam {minutes} menit"
    if minutes:
        return f"{minutes} menit {sec} detik"
    return f"{sec} detik"
