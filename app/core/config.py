from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # database
    database_url: str
    sync_database_url: str
    postgres_user: str
    postgres_password: str
    postgres_db: str

    # logger
    log_level: str = "DEBUG"
    log_dir: str = "logs"
    log_file: str = "app.log"
    log_max_bytes: int = 5 * 1024 * 1024
    log_backup_count: int = 5
    log_format: str = (
        "%(asctime)s | %(levelname)s | %(name)s | "
        "%(funcName)s:%(lineno)d | %(message)s"
    )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
