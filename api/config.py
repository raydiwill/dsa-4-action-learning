from dotenv import load_dotenv
from pathlib import Path
import os


env_path = Path('.') / 'myenv.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "Job Board"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "tdd")
    DATABASE_URL = (f"postgresql://"
                    f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:"
                    f"{POSTGRES_PORT}/{POSTGRES_DB}")


settings = Settings()
