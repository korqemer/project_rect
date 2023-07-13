from dotenv import load_dotenv
import os

load_dotenv()


class Settings():
    database_hostname = os.environ.get("DATABASE_HOSTNAME")
    database_port = os.environ.get("DATABASE_PORT")
    database_password = os.environ.get("DATABSE_PASSWORD")
    database_name = os.environ.get("DATABASE_NAME")
    database_username = os.environ.get("DATABASE_USERNAME")
    secret_key = os.environ.get("SECRET_KEY")
    algorithm = os.environ.get("ALGORITHM")
    access_token_expire_minutes = os.environ.get("TOKEN_EXPIRE_TIME")


settings = Settings()
