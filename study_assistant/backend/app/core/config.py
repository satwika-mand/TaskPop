from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://myuser:mypassword@localhost:5432/studydb"
    gemini_api_key: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
