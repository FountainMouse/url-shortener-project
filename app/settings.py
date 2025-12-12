from pydantic_settings import BaseSettings, SettingsConfigDict
    
class Settings(BaseSettings):
    # Database Settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_HOST: str
    DB_PORT: int
    
    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"
        )

    APP_TTL_MINUTES: int = 1440
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
