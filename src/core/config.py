import os

from pydantic_settings import BaseSettings
from starlette.config import Config

config = Config(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "..", "..", ".env"
    )
)


class Settings(BaseSettings):
    APP_NAME: str = config("APP_NAME", default=None)
    APP_DESCRIPTION: str | None = config("APP_DESCRIPTION", default=None)
    APP_VERSION: str | None = config("APP_VERSION", default=None)
    APP_CONTACT_NAME: str | None = config("APP_CONTACT_NAME", default="WebMaster")
    APP_CONTACT_EMAIL: str | None = config("APP_CONTACT_EMAIL", default="support@example.com")
    APP_LICENSE_NAME: str | None = config("APP_LICENSE_NAME", default="MIT")
    APP_DOCS_ENABLE: bool = config("APP_DOCS_ENABLE", default=False)
    APP_DOCS_SWAGGER_URL: str = config("APP_DOCS_SWAGGER_URL", default="/docs")
    APP_DOCS_REDOC_URL: str = config("APP_DOCS_REDOC_URL", default="/redoc")
    APP_DOCS_OPENAPI_URL: str = config("APP_DOCS_OPENAPI_URL", default="/openapi.json")
    APP_HOST: str = config("APP_HOST", default="127.0.0.1")
    APP_PORT: int = config("APP_PORT", default=8000)
    APP_LOG_LEVEL: str = config("APP_LOG_LEVEL", default="info")
    APP_GENERATE_FIRST_USER_AND_ROLES: bool = config("APP_GENERATE_FIRST_USER_AND_ROLES", default=True)
    APP_USER_DEFAULT_ROLE_CODE: str = config("APP_USER_DEFAULT_ROLE_CODE", default="client")
    APP_EMPLOYER_DEFAULT_ROLE_CODE: str = config("APP_EMPLOYER_DEFAULT_ROLE_CODE", default="employer")
    APP_ADMIN_DEFAULT_ROLE_CODE: str = config("APP_ADMIN_DEFAULT_ROLE_CODE", default="admin")

    JWT_SECRET: str = config("JWT_SECRET")
    JWT_ALGORITHM: str = config("JWT_ALGORITHM", default="HS256")
    JWT_LIFETIME_MINUTES: int = config("JWT_LIFETIME_MINUTES", default=1440)

    POSTGRES_USER: str = config("POSTGRES_USER", default="postgres")
    POSTGRES_PASS: str = config("POSTGRES_PASS", default="postgres")
    POSTGRES_HOST: str = config("POSTGRES_HOST", default="localhost")
    POSTGRES_PORT: int = config("POSTGRES_PORT", default=5432)
    POSTGRES_BASE: str = config("POSTGRES_BASE", default="postgres")
    POSTGRES_URI: str = f"{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_BASE}"

    ADMIN_NAME: str = config("ADMIN_NAME", default="admin")
    ADMIN_EMAIL: str = config("ADMIN_EMAIL", default="admin@uhhhhh.ru")
    ADMIN_USERNAME: str = config("ADMIN_USERNAME", default="admin")
    ADMIN_PASSWORD: str = config("ADMIN_PASSWORD", default="P@ssw0rdUHHHHH")


settings = Settings()