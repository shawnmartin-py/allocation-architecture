from functools import lru_cache

from pydantic import BaseSettings
from sqlalchemy.engine.url import URL


@lru_cache
def get_base_settings():
    class Settings(BaseSettings):
        db_host: str = "localhost"
        db_password: str = "abc123"
        api_host: str = "localhost"
        redis_host: str = "localhost"
        email_host: str = "localhost"

    return Settings()


def get_postgres_uri() -> URL:
    settings = get_base_settings()
    host = settings.db_host
    return URL.create(
        host=host,
        port=54321 if host == "localhost" else 5432,
        password=settings.db_password,
        username="allocation",
        database="allocation",
        drivername="postgresql",
    )


def get_api_url() -> str:
    settings = get_base_settings()
    host = settings.api_host
    port = 5005 if host == "localhost" else 80
    return f"http://{host}:{port}"


def get_redis_host_and_port() -> dict[str]:
    settings = get_base_settings()
    host = settings.redis_host
    port = 63791 if host == "localhost" else 6379
    return dict(host=host, port=port)


def get_email_host_and_port() -> dict[str]:
    settings = get_base_settings()
    host = settings.email_host
    port = 11025 if host == "localhost" else 1025
    http_port = 18025 if host == "localhost" else 8025
    return dict(host=host, port=port, http_port=http_port)
