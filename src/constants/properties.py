import os

from dotenv import load_dotenv

load_dotenv()

SECRET_ACCESS_TOKEN = os.getenv("SECRET_KEY")
SECRET_ALGORITHM = os.getenv("ALGORITHM")
OPENAI_TOKEN = os.getenv("OPENAI_API_TOKEN")
GPT_MODEL = os.getenv("DEPLOYMENT")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")