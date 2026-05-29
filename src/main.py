import argparse
import json
from pathlib import Path

from profile_memory import (
    load_profile,
    save_profile,
    update_profile_from_query,
    format_profile,
)

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    ToolMessage,
    messages_from_dict,
    messages_to_dict,
)

from data_loader import load_dataset
from router import route_query
from agent import build_agent, set_dataframe


MEMORY_DIR = Path("memory")


def load_session_messages(session_id: str):
    MEMORY_DIR.mkdir(exist_ok=True)
    session_path = MEMORY_DIR / f"{session_id}.json"

    if not session_path.exists():
        return []

    with open(session_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return messages_from_dict(data)


def save_session_messages(session_id: str, messages) -> None:
    MEMORY_DIR.mkdir(exist_ok=True)
    session_path = MEMORY_DIR / f"{session_id}.json"

    with open(session_path, "w", encoding="utf-8") as f:
        json.dump(messages_to_dict(messages), f, ensure_ascii=False, indent=2)


def print_reasoning_steps(messages) -> None:
    print("\nReasoning:")
    printed_anything = False

    for msg in messages:
        if isinstance(msg, AIMessage) and msg.tool_calls:
            for tool_call in msg.tool_calls:
                print(f"- Tool call: {tool_call['name']}({tool_call['args']})")
                printed_anything = True

        if isinstance(msg, ToolMessage):
            print(f"- Observation from {msg.name}: {msg.content}")
            printed_anything = True

    if not printed_anything:
        print("- No tool call was needed.")


def get_final_answer(messages) -> str:
    for msg in reversed(messages):
        if isinstance(msg, AIMessage) and not msg.tool_calls:
            return str(msg.content)

    return "I could not produce a final answer."


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--session",
        default="default",
        help="Session ID for persistent conversation memory",
    )
    args = parser.parse_args()

    df = load_dataset()
    set_dataframe(df)

    agent = build_agent()

    conversation_messages = load_session_messages(args.session)
    user_profile = load_profile(args.session)

    print("Customer Service Data Analyst Agent")
    print(f"Session: {args.session}")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("You: ")
        query_lower = query.lower().strip()

        if query_lower in ["exit", "quit"]:
            save_session_messages(args.session, conversation_messages)
            print("Goodbye!")
            break

        user_profile = update_profile_from_query(user_profile, query)
        save_profile(args.session, user_profile)

        if query_lower.startswith("my name is"):
            print("\nReasoning:")
            print("- Updated persistent user profile")
            print("\nAgent:")
            print("Nice to meet you. I will remember your name.")
            print()
            continue

        if query_lower.startswith("i am interested in"):
            print("\nReasoning:")
            print("- Updated persistent user profile")
            print("\nAgent:")
            print("Got it. I will remember this interest.")
            print()
            continue

        if query_lower.startswith("i prefer"):
            print("\nReasoning:")
            print("- Updated persistent user profile")
            print("\nAgent:")
            print("Got it. I will remember this preference.")
            print()
            continue

        if query_lower in [
            "what do you remember about me?",
            "what do you know about me?",
            "what is my profile?",
        ]:
            print("\nReasoning:")
            print("- User asked about persistent user profile")
            print("\nAgent:")
            print(format_profile(user_profile))
            print()
            continue

        query_type = route_query(query)

        if query_type == "out_of_scope":
            print("\nReasoning:")
            print("- Router classified the query as OUT_OF_SCOPE")
            print("Agent: Sorry, I can only answer questions about the customer service dataset.\n")
            continue

        print(f"\nRouter: {query_type.upper()}")

        old_len = len(conversation_messages)
        conversation_messages.append(HumanMessage(content=query))

        try:
            result = agent.invoke(
                {"messages": conversation_messages},
                config={"recursion_limit": 12},
            )
        except Exception as e:
            print("\nAgent:")
            print(f"Sorry, I could not complete the request. Error: {e}")
            continue

        messages = result["messages"]
        new_messages = messages[old_len + 1:]

        print_reasoning_steps(new_messages)

        final_answer = get_final_answer(new_messages)

        print("\nAgent:")
        print(final_answer)
        print()

        conversation_messages = messages
        save_session_messages(args.session, conversation_messages)


if __name__ == "__main__":
    main()