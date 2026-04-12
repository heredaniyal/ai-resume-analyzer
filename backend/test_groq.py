# save as test_groq.py in backend/
import asyncio
from groq import AsyncGroq
import os
from dotenv import load_dotenv

load_dotenv()

async def test():
    client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY"))
    response = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "Say hello in one word"}],
        max_tokens=10
    )
    print(response.choices[0].message.content)

asyncio.run(test())