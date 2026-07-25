from typing import List
from pydantic import BaseModel, Field

from dotenv import load_dotenv
from tavily import TavilyClient
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

load_dotenv()


from shared.search_utils import PROMPT_PATH, LLM

from langchain_tavily import TavilySearch


class Source(BaseModel):
    """Schema for a source used by the agent"""

    url:str =  Field(description="The Url of the source")

class AgentResponse(BaseModel):
    """Schema for the agent response with answer and sources"""

    answer:str = Field(description="The agents answer to the query")
    sources: List[Source] = Field(default_factory=list, description="The list of sources used to generate the answer")



tools=[TavilySearch()]
agent = create_agent(model=LLM, tools=tools, response_format=AgentResponse)

def tavilysearch_pydantic():
    print("Started Websearch using Tavily tool")
    # result = agent.invoke({"messages": HumanMessage(content="What is the weather in Tokyo")})
    result = agent.invoke({"messages": HumanMessage(content="Search 3 job postings for ai engineer using langchain in and around Texas and list their details. These postings should from past 1 week.")})


    print(result)

    
if __name__=="__main__":
    tavilysearch_pydantic()