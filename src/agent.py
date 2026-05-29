import os
from typing import Annotated, Optional

import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from tools import (
    list_categories,
    list_intents,
    count_records,
    show_examples,
    intent_distribution,
)


load_dotenv()

DATAFRAME: Optional[pd.DataFrame] = None


def set_dataframe(df: pd.DataFrame) -> None:
    """
    Store the dataset globally so LangChain tools can access it.
    """
    global DATAFRAME
    DATAFRAME = df


def get_dataframe() -> pd.DataFrame:
    """
    Return the loaded dataset or raise a clear error.
    """
    if DATAFRAME is None:
        raise RuntimeError("Dataset was not loaded. Call set_dataframe(df) first.")
    return DATAFRAME


@tool
def get_categories() -> list[str]:
    """
    Use this tool when the user asks what categories exist in the customer service dataset.
    Returns a list of all unique customer service categories.
    """
    df = get_dataframe()
    return list_categories(df)


@tool
def get_intents(
    category: Annotated[Optional[str], "Optional category to filter intents by"] = None,
) -> list[str]:
    """
    Use this tool when the user asks what intents exist in the dataset.
    If a category is provided, returns only intents from that category.
    """
    df = get_dataframe()
    return list_intents(df, category=category)


@tool
def count_customer_records(
    category: Annotated[Optional[str], "Optional category to filter by, such as REFUND or SHIPPING"] = None,
    intent: Annotated[Optional[str], "Optional intent to filter by, such as get_refund"] = None,
) -> int:
    """
    Use this tool when the user asks how many records, requests, examples, complaints,
    refunds, cancellations, or other customer service cases exist in the dataset.
    You can filter by category and/or intent.
    """
    df = get_dataframe()
    return count_records(df, category=category, intent=intent)

@tool
def count_by_category(
    category: Annotated[str, "Customer service category, such as REFUND, SHIPPING, ACCOUNT"],
) -> int:
    """
    Use this tool when the user asks how many requests or records exist in a whole category.
    For example: 'How many refund requests did we get?' should use category='REFUND'.
    Do not use an intent unless the user explicitly asks for a specific intent.
    """
    df = get_dataframe()
    return count_records(df, category=category)

@tool
def get_examples(
    category: Annotated[Optional[str], "Optional category to filter by"] = None,
    intent: Annotated[Optional[str], "Optional intent to filter by"] = None,
    n: Annotated[int, "Number of examples to return"] = 3,
) -> list[dict]:
    """
    Use this tool when the user asks to see example customer messages or agent responses.
    You can filter examples by category, intent, or both.
    """
    df = get_dataframe()
    return show_examples(df, category=category, intent=intent, n=n)


@tool
def get_intent_distribution(
    category: Annotated[str, "Category for which to calculate the intent distribution"],
) -> dict[str, int]:
    """
    Use this tool when the user asks for the distribution of intents within a category.
    """
    df = get_dataframe()
    return intent_distribution(df, category=category)


def build_agent():
    """
    Build the LangGraph ReAct agent.
    """
    api_key = os.getenv("NEBIUS_API_KEY")

    if not api_key:
        raise RuntimeError("Missing NEBIUS_API_KEY in .env file.")

    llm = ChatOpenAI(
        model="meta-llama/Llama-3.3-70B-Instruct",
        api_key=api_key,
        base_url="https://api.studio.nebius.com/v1/",
        temperature=0,
    )

    tools = [
        get_categories,
        get_intents,
        count_by_category,
        count_customer_records,
        get_examples,
        get_intent_distribution,
    ]

    system_prompt = """
You are a customer service dataset analyst.

You can answer only questions about the Bitext customer service dataset.
Use tools whenever the user asks for counts, categories, intents, examples, or distributions.

Important memory rule:
If the user asks a follow-up question such as "show me more", "show me 3 more",
"what about refunds?", or "what is the total count of the last two?",
use the previous conversation messages to infer the missing category, intent, or operation.
Do not switch to another category unless the user explicitly asks for it.

For open-ended summaries, first use tools to inspect relevant examples, then summarize based only on the dataset.
If the user asks something unrelated to the dataset, politely decline.

Always be concise and data-grounded.
"""

    return create_react_agent(
        model=llm,
        tools=tools,
        state_modifier=system_prompt,
    )