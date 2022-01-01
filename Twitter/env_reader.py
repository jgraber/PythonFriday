# pip install python-dotenv
import os
from dotenv import load_dotenv

database_url = os.getenv('DATABASE_URL')
print(database_url)

load_dotenv()

database_url = os.getenv('DATABASE_URL', 'sqlite://')
print(database_url)