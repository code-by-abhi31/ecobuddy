import os
from groq import Groq
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Initialize the raw Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Fetch and print all active models
print("--- ACTIVE GROQ MODELS ---")
models = client.models.list()
for m in models.data:
    print(m.id)
print("--------------------------")