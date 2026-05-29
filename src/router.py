from typing import Literal


QueryType = Literal["structured", "unstructured", "out_of_scope"]


def route_query(query: str) -> QueryType:
    """
    Simple rule-based router.
    Later we can replace this with an LLM router.
    """
    q = query.lower()

    out_of_scope_keywords = [
        "president",
        "champions league",
        "poem",
        "crm software",
        "weather",
        "movie",
        "song",
    ]

    unstructured_keywords = [
        "summarize",
        "typically respond",
        "how do agents respond",
        "explain",
        "describe",
        "remember",
        "memory",
        "discuss before",
        "previous",
        "earlier",
        "before",
    ]

    structured_keywords = [
        "how many",
        "count",
        "categories",
        "intents",
        "distribution",
        "examples",
        "show me",
    ]

    if any(keyword in q for keyword in out_of_scope_keywords):
        return "out_of_scope"

    if any(keyword in q for keyword in unstructured_keywords):
        return "unstructured"

    if any(keyword in q for keyword in structured_keywords):
        return "structured"

    return "out_of_scope"