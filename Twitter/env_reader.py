# pip install python-dotenv
import os
from dotenv import load_dotenv

database_url = os.getenv('DATABASE_URL')
print(database_url)

# loads .env file into application environment
load_dotenv()

database_url = os.getenv('DATABASE_URL')
print(database_url)