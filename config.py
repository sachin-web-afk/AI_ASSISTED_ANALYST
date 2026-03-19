import os
from dotenv import load_dotenv

load_dotenv(".env")

class Config:

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    DATABRICKS_SERVER_HOSTNAME = os.getenv("DATABRICKS_SERVER_HOSTNAME")
    DATABRICKS_HTTP_PATH = os.getenv("DATABRICKS_HTTP_PATH")
    DATABRICKS_ACCESS_TOKEN = os.getenv("DATABRICKS_ACCESS_TOKEN")