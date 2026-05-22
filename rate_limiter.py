from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    telegram_bot_token: str = ""
    gemini_api_key: str = ""
    groq_api_key: str = ""
    openai_compatible_api_key: str = ""
    default_model_order: str = "gemini-2.0-flash,groq-llama,openai-compatible"
    database_path: str = "quota_guard.db"

    @property
    def model_order(self) -> list[str]:
        return [m.strip() for m in self.default_model_order.split(",") if m.strip()]

    class Config:
        env_file = ".env"


settings = Settings()
