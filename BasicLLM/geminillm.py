from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input="Hello Google"
)
print(interaction.output_text)