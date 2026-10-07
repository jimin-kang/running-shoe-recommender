from pathlib import Path

from pydantic_settings import BaseSettings # manages app config & env vars

PROJECT_ROOT = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    database_path: Path = PROJECT_ROOT / "data"/ "shoes.db"


settings = Settings()
print(f"SETTINGS: {settings}")