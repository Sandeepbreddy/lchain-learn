from dotenv import load_dotenv
from tavily import TavilyClient
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

load_dotenv()


from shared.search_utils import PROMPT_PATH, LLM

tavily = TavilyClient()

@tool
def search(query: str) -> str:

    """Search the web for information based on a query."""

    print(f"Searching for {query}")

    # return "Tokyo weather is sunny"
    return tavily.search(query=query)

with open(PROMPT_PATH/'basic_search.md', 'r') as f:
    prompt = f.read()

tools=[search]
agent = create_agent(model=LLM, tools=tools, system_prompt=prompt)

def websearch():
    print("Started Websearch using Tavily tool")
    # result = agent.invoke({"messages": HumanMessage(content="What is the weather in Tokyo")})
    result = agent.invoke({"messages": HumanMessage(content="Search 3 job postings for ai engineer using langchain in around USA where H1B visa is sponsored on linkedin and list their details")})


    print(result)
if __name__=="__main__":
    websearch()