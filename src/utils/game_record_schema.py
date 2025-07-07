from datetime import datetime, timezone

def build_chat_record(game_id, game_name, messages):
    if not isinstance(game_id, str):
        raise ValueError("game_id must be a string")
    if not isinstance(game_name, str):
        raise ValueError("game_name must be a string")
    if not isinstance(messages, list) or not all(isinstance(m, str) for m in messages):
        raise ValueError("messages must be a list of strings")

    return {
        "game_id": game_id,
        "game_name": game_name,
        "game_active": True,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "messages": messages,
    }

def parse_chat_record(record):
    return {
        "game_id": record.get("game_id", ""),
        "game_name": record.get("game_name", ""),
        "messages": record.get("messages", []),
        "game_active": record.get("game_active", True),
        "created_at": record.get("created_at", ""),
    }