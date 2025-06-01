def build_user_record(user_id, active_games):
    if not isinstance(user_id, str):
        raise ValueError("user_id must be a string")
    if not isinstance(active_games, list) or not all(
        isinstance(g, dict) and isinstance(g.get("id"), str) and isinstance(g.get("name"), str)
        for g in active_games
    ):
        raise ValueError("active_games must be a list of dicts with 'id' and 'name' as strings")

    return {
        "user_id": user_id,
        "active_games": active_games
    }

def parse_user_record(record):
    return {
        "user_id": record.get("user_id", ""),
        "active_games": record.get("active_games", [])
    }