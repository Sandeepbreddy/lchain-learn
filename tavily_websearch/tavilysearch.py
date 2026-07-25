from dotenv import load_dotenv
from tavily import TavilyClient
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

load_dotenv()


from shared.search_utils import PROMPT_PATH, LLM

from langchain_tavily import TavilySearch

tools=[TavilySearch()]
agent = create_agent(model=LLM, tools=tools)

def tavilyearch():
    print("Started Websearch using Tavily tool")
    # result = agent.invoke({"messages": HumanMessage(content="What is the weather in Tokyo")})
    result = agent.invoke({"messages": HumanMessage(content="Search 3 job postings for ai engineer using langchain in and around Texas and list their details. These postings should from past 1 week.")})


    print(result)

    
if __name__=="__main__":
    tavilyearch()