from typing import Optional
from pydantic import BaseModel, Field
import pandas as pd


class CategoryInput(BaseModel):
    category: str = Field(description="Customer service category, for example REFUND, SHIPPING, ACCOUNT")


class ExamplesInput(BaseModel):
    category: Optional[str] = Field(default=None, description="Category to filter by")
    intent: Optional[str] = Field(default=None, description="Intent to filter by")
    n: int = Field(default=3, description="Number of examples to return")


class DistributionInput(BaseModel):
    category: str = Field(description="Category for which to calculate intent distribution")


class CountInput(BaseModel):
    category: Optional[str] = Field(default=None, description="Category to filter by")
    intent: Optional[str] = Field(default=None, description="Intent to filter by")


def list_categories(df: pd.DataFrame) -> list[str]:
    """
    Return all unique categories in the dataset.
    """
    return sorted(df["category"].dropna().unique().tolist())


def list_intents(df: pd.DataFrame, category: Optional[str] = None) -> list[str]:
    """
    Return all unique intents, optionally filtered by category.
    """
    temp = df.copy()

    if category:
        temp = temp[temp["category"].str.upper() == category.upper()]

    return sorted(temp["intent"].dropna().unique().tolist())


def count_records(
    df: pd.DataFrame,
    category: Optional[str] = None,
    intent: Optional[str] = None,
) -> int:
    """
    Count rows in the dataset, optionally filtered by category and/or intent.
    """
    temp = df.copy()

    if category:
        temp = temp[temp["category"].str.upper() == category.upper()]

    if intent:
        temp = temp[temp["intent"].str.upper() == intent.upper()]

    return len(temp)


def show_examples(
    df: pd.DataFrame,
    category: Optional[str] = None,
    intent: Optional[str] = None,
    n: int = 3,
) -> list[dict]:
    """
    Show example customer requests from the dataset.
    """
    temp = df.copy()

    if category:
        temp = temp[temp["category"].str.upper() == category.upper()]

    if intent:
        temp = temp[temp["intent"].str.upper() == intent.upper()]

    cols = [col for col in ["instruction", "response", "category", "intent"] if col in temp.columns]

    return temp[cols].head(n).to_dict(orient="records")


def intent_distribution(df: pd.DataFrame, category: str) -> dict[str, int]:
    """
    Return the distribution of intents within a category.
    """
    temp = df[df["category"].str.upper() == category.upper()]

    return (
        temp["intent"]
        .value_counts()
        .to_dict()
    )