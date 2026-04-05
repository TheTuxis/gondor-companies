from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    PORT: int = 8019
    DATABASE_URL: str = "postgresql+asyncpg://gondor:gondor_dev@localhost:5432/gondor_companies"
    JWT_SECRET: str = "local-dev-secret-change-in-production"
    REDIS_URL: str = "redis://localhost:6379"
    NATS_URL: str = "nats://localhost:4222"
    LOG_LEVEL: str = "info"
    ENVIRONMENT: str = "development"


settings = Settings()
