from pydantic import BaseSettings


class Settings(BaseSettings):
    """Server config settings"""

    # Mongo Engine settings
    MONGO_HOST: str = "localhost"
    MONGO_PORT: int = 27117
    MONGO_INITDB_ROOT_USERNAME: str = "test"
    MONGO_INITDB_ROOT_PASSWORD: str = "test"
    MONGO_DB_NAME: str = "test"
    MONGO_URI: str = (
        f"mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB_NAME}"
    )

    # Security settings
    AUTHJWT_SECRET_KEY: str = "secret"
    SALT: str = "$2b$12$GeBAcXwm5tCsWVf2992qdO"

    DEV_MODE: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
