from functools import lru_cache
from typing import List
from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore', case_sensitive=False)

    APP_NAME: str = 'Nivara AI'
    API_VERSION: str = '2.1.0'
    SECRET_KEY: str = 'change-this-in-production'
    ANTHROPIC_API_KEY: str = ''
    DATABASE_URL: str = 'sqlite:///./data/nivara.db'
    ENVIRONMENT: str = 'development'
    CORS_ORIGINS: str = 'http://localhost:5173,http://localhost:3000'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = 'HS256'
    SEED_DEMO_DATA: bool = False
    MARKET_DATA_MODE: str = 'development'
    RATE_LIMIT_PER_MINUTE: int = 120
    AUTO_CREATE_SCHEMA: bool = True

    @field_validator('ACCESS_TOKEN_EXPIRE_MINUTES')
    @classmethod
    def validate_token_lifetime(cls, value: int) -> int:
        if value < 5 or value > 1440:
            raise ValueError('ACCESS_TOKEN_EXPIRE_MINUTES must be between 5 and 1440')
        return value

    @field_validator('RATE_LIMIT_PER_MINUTE')
    @classmethod
    def validate_rate_limit(cls, value: int) -> int:
        if value < 10 or value > 10000:
            raise ValueError('RATE_LIMIT_PER_MINUTE must be between 10 and 10000')
        return value

    @model_validator(mode='after')
    def validate_production(self):
        if self.ENVIRONMENT.lower() == 'production':
            if len(self.SECRET_KEY) < 32 or self.SECRET_KEY == 'change-this-in-production':
                raise ValueError('Production requires a strong SECRET_KEY of at least 32 characters')
            if '*' in self.cors_origins_list:
                raise ValueError('Wildcard CORS origins are not allowed in production')
            if self.SEED_DEMO_DATA:
                raise ValueError('SEED_DEMO_DATA must be disabled in production')
            if self.AUTO_CREATE_SCHEMA:
                raise ValueError('AUTO_CREATE_SCHEMA must be disabled in production; use Alembic migrations')
        return self

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(',') if o.strip()]

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
