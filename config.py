import os

from dotenv import load_dotenv

load_dotenv()

PROXY_HOST = os.getenv('PROXY_HOST')
PROXY_PORT = os.getenv('PROXY_PORT')
PROXY_USER = os.getenv('PROXY_LOGIN')
PROXY_PASS = os.getenv('PROXY_PASSWORD')
