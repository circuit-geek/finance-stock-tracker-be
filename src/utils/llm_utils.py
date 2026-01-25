import json

from openai import OpenAI
from src.constants.properties import OPENAI_TOKEN

client = OpenAI(api_key=OPENAI_TOKEN)