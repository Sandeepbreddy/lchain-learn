import os

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

load_dotenv()

def main():
    print("Hello from lchain-learn!")
    print(os.environ.get("OPENAI_API_KEY"))



if __name__ == "__main__":
    main()
