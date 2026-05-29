import sys
from pathlib import Path
from typing import Optional

from fastmcp import FastMCP

sys.path.append(str(Path(__file__).parent / "src"))

from data_loader import load_dataset
from tools import (
    list_categories,
    list_intents,
    count_records,
    show_examples,
    intent_distribution,
)


mcp = FastMCP("Customer Service Data Analyst MCP Server")

df = load_dataset()


@mcp.tool()
def get_categories() -> list[str]:
    """
    Return all categories in the Bitext customer service dataset.
    """
    return list_categories(df)


@mcp.tool()
def count_by_category(category: str) -> int:
    """
    Count how many records exist in a customer service category.
    Example category: REFUND, SHIPPING, ACCOUNT.
    """
    return count_records(df, category=category)


@mcp.tool()
def get_examples(
    category: Optional[str] = None,
    intent: Optional[str] = None,
    n: int = 3,
) -> list[dict]:
    """
    Return example customer requests and agent responses.
    Can filter by category, intent, or both.
    """
    return show_examples(df, category=category, intent=intent, n=n)


@mcp.tool()
def get_intent_distribution(category: str) -> dict[str, int]:
    """
    Return the distribution of intents inside a given category.
    """
    return intent_distribution(df, category=category)


@mcp.tool()
def get_intents(category: Optional[str] = None) -> list[str]:
    """
    Return all intents, optionally filtered by category.
    """
    return list_intents(df, category=category)


if __name__ == "__main__":
    mcp.run()