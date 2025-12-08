from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.azure import AzureProvider
from src.constants.properties import GPT_MODEL, OPENAI_ENDPOINT, OPENAI_API_VERSION, OPENAI_TOKEN

azure_model = OpenAIChatModel(
    model_name=GPT_MODEL,
    provider= AzureProvider (
        azure_endpoint= OPENAI_ENDPOINT,
        api_version= OPENAI_API_VERSION,
        api_key= OPENAI_TOKEN
    ),
)
