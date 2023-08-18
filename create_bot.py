import os
import sys

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from aiohttp import web
from dotenv import load_dotenv
from DAO.postgres import PostgresDao
from loguru import logger
from keycloak import KeycloakOpenID

load_dotenv()

TOKEN_API = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_DOMAIN = os.getenv("WEBHOOK_DOMAIN")

keycloak_server_url = os.getenv("KC_SERVER_URL")
keycloak_client_id = os.getenv("KC_CLIENT_ID")
keycloak_realm_name = os.getenv("KC_REALM_NAME")
keycloak_client_secret_key = os.getenv("KC_CLIENT_SECRET_KEY")

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_database = os.getenv("DB_DATABASE")

DEBUG = os.getenv("DEBUG").lower() in ('true', '1', 't')

if not DEBUG:
    logger.remove()
    logger.add(sys.stderr, level="INFO")

bot = Bot(token=TOKEN_API)
Bot.set_current(bot)
dp = Dispatcher(bot, storage=MemoryStorage())
Dispatcher.set_current(dp)

db = PostgresDao(db_user, db_password, db_host, db_port, db_database)

kc = KeycloakOpenID(server_url=keycloak_server_url,
                    client_id=keycloak_client_id,
                    realm_name=keycloak_realm_name,
                    client_secret_key=keycloak_client_secret_key)

app = web.Application()
