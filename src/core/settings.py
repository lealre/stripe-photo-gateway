from pathlib import Path

from pydantic import DirectoryPath, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='allow'
    )

    BACKEND_DOMAIN: str = 'http://127.0.0.1:8000'

    DATABASE_URL: str = 'sqlite+aiosqlite:///./dev.db'

    HOST_EMAIL: str = 'renaanvp@gmail.com'

    EMAIL_USERNAME: str = ''
    EMAIL_PASSWORD: SecretStr = SecretStr('')
    EMAIL_FROM: str = ''
    EMAIL_PORT: int = 587
    EMAIL_SERVER: str = ''
    EMAIL_FROM_NAME: str = ''
    EMAIL_STARTTLS: bool = True
    EMAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    TEMPLATE_FOLDER: DirectoryPath = Path('src/integrations/email/templates')

    GOOGLE_API_KEY: str = ''
    GOOGLE_CLIENT_ID: str = ''
    GOOGLE_CLIENT_SECRET: str = ''
    GOOGLE_VALIDATION_API_URL: str = ''

    REDIS_URL: str = 'redis://localhost:6379/0'
    REDIS_EXPIRATION_TIME: int = 86400
    REDIS_BROKER_URL: str = 'redis://localhost:6379/1'

    STRIPE_API_KEY: str = ''

    AWS_ACCESS_KEY: str = ''
    AWS_SECRET_KEY: str = ''
    AWS_REGION: str = ''
    AWS_S3_BUCKET_NAME: str = ''

    STRIPE_PRICE_ID: str = ''


settings = Settings()
