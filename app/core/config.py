from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Wallet API'
    app_description: str = 'REST API for wallet operations'

    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: int
    database_url: str
    database_url_local: str

    class Config:
        env_file = '.env'


settings = Settings()
