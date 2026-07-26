from dotenv import load_dotenv

load_dotenv()

# from _typeshed import OpenBinaryMode



from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage


from langsmith import traceable

MAX_ITERATIONS = 10

@tool
def get_product_price(product: str) -> float:
    """Look up the price of a product in the catalog"""
    print(f".  >> Executing get_product_price(product='{product}')")

    prices={"laptop":1299.99, "headphones": 149.95, "keyboard":29.99}

    return prices.get(product, 0)

@tool
def apply_discount(price: float, discount_tier: str) -> float:
    """Apply a discount tier to a price and return a final price.
    Available tiers: bronze, silver and gold.
    """
    print(f"   >> Executing apply_discount(price={price}, discount_tier={discount_tier})")

    discount_percentages = {"bronze": 5, "silver": 9, "gold": 12}

    discount = discount_percentages.get(discount_tier, 0)
    return round(price * (1-discount/ 100), 2)


#Agent - loop
@traceable(name="Langchain Agent Loop")
def run_agent(question: str):
    tools = [get_product_price, apply_discount]
    tool_dict = {t.name: t for t in tools}
    llm = init_chat_model(model='openai:gpt-5.5', temperature = 0)
    llm_with_tools = llm.bind_tools(tools)

    print(f"Question: {question}")
    print("="*20)

    messages = [
        SystemMessage(
            content="""
                    You are helpful shopping assistant.
                    You have access to product catalog tool and discount tool.
                    STRICT RULES - You must follow these exactly.
                    1. Never assume or guess any product price.
                    2. You must call get_product_price first to get the real price.
                    3. Only call apply_discount AFTER you have received price from get_product_price.
                    4. Pass the exact price returned by get_product_price. -> DO NOT PASS MADE UP NUMBER
                    5. NEVER CALCULATE DISCOUNTS YOURSELF.
                    6. IF USER DID NOT SPECIFY DISCOUNT TIER ASK THEM TO USE - DO NOT ASSUME ONE
                    """
        ),
        HumanMessage(content=question)
    ]

    for iteration in range(1, MAX_ITERATIONS + 1):
        print(f"\n--Iteration - {iteration}--")
        ai_message = llm_with_tools.invoke(messages)

        tool_calls = ai_message.tool_calls

        #If not tool calls this is final answer
        if not tool_calls:
            print(f"\n Final Answer: {ai_message.content}")
            return ai_message.content

        #Process only first tool call. We are forcing it

        tool_call = tool_calls[0]
        tool_name = tool_call.get("name")
        tool_args = tool_call.get("args")
        tool_call_id = tool_call.get("id")

        print(f" [Tool Selected] {tool_name} with args: {tool_args}")

        tool_to_use = tool_dict.get(tool_name)

        if tool_to_use is None:
            raise ValueError("Tool '{tool_name}' not found")

        observation = tool_to_use.invoke(tool_args)

        print(f"[Tool Result] : {observation}")

        print(f"{tool_call_id}")

        messages.append(ai_message)
        messages.append(
            ToolMessage(content=str(observation), tool_call_id = tool_call_id)
        )
    print("ERROR - Max Iternations reached without any final answer")
    return None

if __name__ == "__main__":
    print(f"Hello Langchain Agent (.bind_tools)!")
    print()

    result = run_agent("What is the price of the laptop after applying a gold discount")

