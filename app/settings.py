from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "postgresql://mikheevaD:password@localhost:5432/question_db"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()