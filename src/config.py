from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Self
from pydantic import model_validator


class PostgresSettings(BaseSettings):
    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_pass: str

    db_dsn: str = ''
    db_dsn_sync: str = ''

    @model_validator(mode='after')
    def db_dsn_validate(self) -> Self:
        self.db_dsn = (f'postgresql+asyncpg://'
                       f'{self.postgres_user}:{self.postgres_pass}@'
                       f'{self.postgres_host}:{self.postgres_port}/'
                       f'{self.postgres_db}')

        self.db_dsn_sync = (f'postgresql+psycopg://'
                            f'{self.postgres_user}:{self.postgres_pass}@'
                            f'{self.postgres_host}:{self.postgres_port}/'
                            f'{self.postgres_db}')
        return self


class RedisSettings(BaseSettings):
    redis_host: str
    redis_port: int
    redis_databases: int
    redis_password: str


class Settings(BaseSettings):
    postgres: PostgresSettings

    redis: RedisSettings

    model_config = SettingsConfigDict(
        env_nested_delimiter='__',
        env_file='.env',
        env_file_encoding='utf8',
        extra='ignore'
    )


settings = Settings()  # type: ignore
