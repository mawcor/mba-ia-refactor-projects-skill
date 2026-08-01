import os

SECRET_KEY = os.environ.get("SECRET_KEY", "minha-chave-super-secreta-123")
DEBUG = os.environ.get("DEBUG", "True").lower() in ("true", "1", "t")
DB_PATH = os.environ.get("DB_PATH", "loja.db")
