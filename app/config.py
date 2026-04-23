from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Fallback local pour démarrer sans PostgreSQL:
    # définir DATABASE_URL pour pointer vers PostgreSQL.
    database_url: str = "sqlite+pysqlite:///./odd_arrdel.db"


settings = Settings()

