from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

information = """
    Give some information about OPENAI Creator. I may ask question on top of this. Summarize the answers in 8 -10 sentences. Add two interesting facts about them.
    Is the creator {Creator}
""" 

summary_prompt_template = PromptTemplate(
    input_variables=["Creator"], template=information
)

llm = ChatOpenAI(temperature=0, model="gpt-5")

chain = summary_prompt_template | llm

response = chain.invoke(input={"Creator": "elonmusk"})

print(f"Response from LLM {response.content}")


