import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    models = client.models.list()
    print("✅ API Key is valid!")
    for m in models.data[:5]:
        print("-", m.id)
except Exception as e:
    print("❌ Key not working:", e)
