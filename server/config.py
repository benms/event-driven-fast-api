from pydantic import BaseSettings


class Settings(BaseSettings):
    front_url: str = 'http://localhost:3000'
    server_host: str = '127.0.0.1'
    server_port: int = 8000
    redis_host: str = ''
    redis_port: int = 1234
    redis_password: str = ''

    class Config:
      env_file = ".env"

config = Settings()
