import json
from pathlib import Path


PROFILE_DIR = Path("profiles")


def load_profile(session_id: str) -> dict:
    PROFILE_DIR.mkdir(exist_ok=True)
    path = PROFILE_DIR / f"{session_id}.json"

    if not path.exists():
        return {
            "name": None,
            "interests": [],
            "preferences": [],
        }

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_profile(session_id: str, profile: dict) -> None:
    PROFILE_DIR.mkdir(exist_ok=True)
    path = PROFILE_DIR / f"{session_id}.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)


def update_profile_from_query(profile: dict, query: str) -> dict:
    q = query.lower()

    if "my name is" in q:
        name = q.split("my name is", 1)[1].strip().split()[0]
        profile["name"] = name.capitalize()

    if "i am interested in" in q:
        interest = q.split("i am interested in", 1)[1].strip()
        if interest and interest not in profile["interests"]:
            profile["interests"].append(interest)

    if "i prefer" in q:
        preference = q.split("i prefer", 1)[1].strip()
        if preference and preference not in profile["preferences"]:
            profile["preferences"].append(preference)

    return profile


def format_profile(profile: dict) -> str:
    lines = []

    if profile.get("name"):
        lines.append(f"Name: {profile['name']}")

    if profile.get("interests"):
        lines.append("Interests: " + ", ".join(profile["interests"]))

    if profile.get("preferences"):
        lines.append("Preferences: " + ", ".join(profile["preferences"]))

    if not lines:
        return "I do not remember any user profile details yet."

    return "\n".join(lines)