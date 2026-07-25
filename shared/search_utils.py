from pathlib import Path
from langchain_openai import ChatOpenAI

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROMPT_PATH=PROJECT_ROOT/'Prompts'

LLM = ChatOpenAI(temperature=0, model="gpt-5")