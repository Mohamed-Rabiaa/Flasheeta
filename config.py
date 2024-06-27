import os
import logging

# setting the config for debuging 
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[
                        logging.FileHandler("app.log"),  # Log to a file
                        logging.StreamHandler()  # Also log to the console
                    ])


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "Can you guess it?"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://flasheeta_dev:flasheeta_pwd@localhost/flasheeta_dev_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
