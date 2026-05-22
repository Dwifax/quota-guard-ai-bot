import httpx

from app.config import settings
from app.rate_limiter import is_rate_limit_error
from app.storage import is_on_cooldown, set_cooldown


class ProviderError(Exception):
    pass


class RateLimitedError(ProviderError):
    def __init__(self, provider: str, message: str):
        self.provider = provider
        super().__init__(message)


async def call_gemini(prompt: str) -> str:
    if not settings.gemini_api_key:
        raise ProviderError("GEMINI_API_KEY belum diisi.")

    # Placeholder endpoint supaya aman untuk starter repo.
    # Ganti dengan endpoint resmi yang kamu pakai.
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
            params={"key": settings.gemini_api_key},
            json={"contents": [{"parts": [{"text": prompt}]}]},
        )

    if response.status_code == 429 or is_rate_limit_error(response.text):
        raise RateLimitedError("gemini-2.0-flash", response.text)

    response.raise_for_status()
    data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]


async def call_mock_provider(prompt: str, provider: str) -> str:
    return f"[{provider}] Demo response untuk prompt: {prompt}"


async def ask_ai(prompt: str) -> str:
    errors: list[str] = []

    for provider in settings.model_order:
        cooldown, remaining, reason = is_on_cooldown(provider)
        if cooldown:
            errors.append(f"{provider} cooldown {remaining}s: {reason}")
            continue

        try:
            if provider.startswith("gemini"):
                return await call_gemini(prompt)
            return await call_mock_provider(prompt, provider)

        except RateLimitedError as exc:
            set_cooldown(provider, 60 * 30, "Rate limited / quota exhausted")
            errors.append(f"{provider}: {exc}")
        except Exception as exc:
            errors.append(f"{provider}: {exc}")

    return "Semua provider gagal atau sedang cooldown.\n" + "\n".join(errors)
