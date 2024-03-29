import os
from functools import lru_cache
from os import getenv
from typing import Optional

from dotenv import load_dotenv
from pydantic import Field, BaseSettings, PostgresDsn, validator

from controllers.files_controller import FileController


def check_env_exist():
    if not os.path.exists('.env'):
        try:
            os.mknod('.env')
        except Exception as error:
            raise Exception(f'No .env file: {error}')


def write_env(key: str, value: str | int) -> None:
    with open('.env', 'a') as env_file:
        env_file.write(f'\n{key}={value}')


class Settings(BaseSettings):
    check_env_exist()
    load_dotenv()

    PROJECT_NAME: str = Field(default='name error')
    VERSION: str = Field(default='error')
    DEBUG: bool = Field(default=True)
    VK_PROCESS_DEBUG: bool = Field(default=True)

    SECRET: str = Field(default='SECRET')

    SERVER_HOST: str = Field(default='localhost')
    SERVER_PORT: int = Field(default=443)

    POSTGRES_DB: str = Field(default='database')
    POSTGRES_USER: str = Field(default='root')
    POSTGRES_PASSWORD: str = Field(default='root_password')
    POSTGRES_HOST: str = Field(default='localhost')
    POSTGRES_PORT: str = Field(default='5432')

    ADMINER_PORT: int = Field(default=2087)

    MAX_FILE_SIZE: int = Field(default=10)
    CURRENT_FILE_PATH: str = Field(default='')
    CURRENT_FILE_NAME: int = Field(default=0)

    SSL_DATA: dict = Field(default={
        'ssl_keyfile': getenv('SSL_KEYFILE'),
        'ssl_certfile': getenv('SSL_CERTFILE')
    })

    SQLALCHEMY_URL: Optional[PostgresDsn] = None

    CODE_IMAGE_CONTROLLER: FileController = Field(default=FileController('files/code'))

    @validator('SQLALCHEMY_URL', pre=True)
    def get_sqlalchemy_url(cls, v, values):
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            user=values.get('POSTGRES_USER'),
            password=values.get('POSTGRES_PASSWORD'),
            host=values.get('POSTGRES_HOST'),
            port=values.get('POSTGRES_PORT'),
            path=f'/{values.get("POSTGRES_DB")}'
        )

    @validator('SERVER_HOST', pre=True)
    def check_debug_mode(cls, v, values):
        if values.get('DEBUG'):
            return 'localhost'
        return v


@lru_cache
def get_settings() -> Settings:
    return Settings()
