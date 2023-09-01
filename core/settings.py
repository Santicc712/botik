from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str
    admin_id: int


@dataclass
class Db:
    db_host: str
    db_database: str
    db_user: str
    dp_password: str


@dataclass
class Settings:
    bots: Bots
    db: Db


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str('TOKEN'),
            admin_id=env.int('ADMIN_ID')
        ),
        db=Db(
            db_host=env.str("DB_HOST"),
            db_database=env.str("DB_DATABASE"),
            db_user=env.str("DB_USER"),
            dp_password=env.str("DB_PASSWORD")
        )
    )


settings = get_settings('input')