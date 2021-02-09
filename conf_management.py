import psycopg2
import os
import sys

def get_telegram_token():
    return os.getenv('TELEGRAM_TOKEN')


def get_telegram_group_id():
    print ('TELEGRAM_GROUP_ID=' + os.getenv('TELEGRAM_GROUP_ID'))
    return os.getenv('TELEGRAM_GROUP_ID')


def get_connection_by_config():
    postgresql = {
        "host": os.getenv('localhost'),
        "user": os.getenv('postgres'),
        "password": os.getenv('748596alex'),
        "database": os.getenv('Rotu_Go_bot'),
        "port": "5432"
    }
    conn = psycopg2.connect(**postgresql)
    return conn