def build_chat_record(game_id, game_name, original_message, messages):
    if not isinstance(game_id, str):
        raise ValueError("game_id must be a string")
    if not isinstance(game_name, str):
        raise ValueError("game_name must be a string")
    if not isinstance(original_message, str):
        raise ValueError("original_message must be a string")
    if not isinstance(messages, list) or not all(isinstance(m, str) for m in messages):
        raise ValueError("messages must be a list of strings")

    return {
        "game_id": game_id,
        "game_name": game_name,
        "original_message": original_message,
        "messages": messages
    }

def parse_chat_record(record):
    return {
        "game_id": record.get("game_id", ""),
        "game_name": record.get("game_name", ""),
        "original_message": record.get("original_message", ""),
        "messages": record.get("messages", [])
    }