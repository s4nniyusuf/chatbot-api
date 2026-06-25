import redis
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)


def save_history(user_id: str, history: list[dict]):
    r.set(f"chat: {user_id}", json.dumps(history))


def get_history(user_id: str) -> list[dict]:
    history = r.get(f"chat: {user_id}")
    if history:
        return json.loads(history)
    return []