import os
from dotenv import load_dotenv

# Get the directory where this file is located
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# The .env file is one level above this file
ENV_FILE = os.path.join(CURRENT_DIR, "..", ".env")

#Load environment variables from the .env file
load_dotenv(ENV_FILE)

LLM_PROVIDER = os.getenv("LLM_PROVIDER")
LLM_MODEL = os.getenv("LLM_MODEL")

# Read the LLM API key
LLM_API_KEY = os.getenv("LLM_API_KEY")

# Default model to use throughout the application
MODEL_NAME = "gpt-5-mini"

# Validate that the API key exists
if not LLM_API_KEY:
    raise RuntimeError(
        "LLM_API_KEY not found. Please check your .env file"
    )
