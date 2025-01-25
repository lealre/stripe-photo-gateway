from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='allow'
    )

    BACKEND_DOMAIN: str = 'http://127.0.0.1:8000'

    DATABASE_URL: str = 'sqlite+aiosqlite:///./dev.db'

    REDIS_URL: str = 'redis://localhost:6379/0'
    REDIS_EXPIRATION_TIME: int = 86400
    REDIS_BROKER_URL: str = 'redis://localhost:6379/1'


settings = Settings()
