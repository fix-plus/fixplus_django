import json
from django.core.cache import cache
from src.chat.models import ChatMessage
from typing import Optional


def save_message_to_cache(message: ChatMessage) -> None:
    """
    Save a chat message to Redis cache using a list structure.
    Args:
        message: ChatMessage instance to be cached.
    """
    cache_key = f"chat_messages_{message.room_id}"
    cache_data = {
        "id": str(message.id),
        "room_id": str(message.room_id),
        "user_id": str(message.user_id),
        "text": message.text,
        "file_id": str(message.file_id) if message.file_id else None,
        "replied_from_id": str(message.replied_from_id) if message.replied_from_id else None,
        "is_delivered": message.is_delivered,
        "is_read": message.is_read,
        "is_deleted": message.is_deleted,
        "is_system_message": message.is_system_message,
        "read_at": int(message.read_at.timestamp()) if message.read_at else None,
        "timestamp": int(message.timestamp.timestamp())
    }
    try:
        redis_client = cache.client.get_client()
        redis_client.lpush(cache_key, json.dumps(cache_data, ensure_ascii=False))
        # Set expiration for cache key to prevent unlimited growth (e.g., 7 days)
        redis_client.expire(cache_key, 7 * 24 * 60 * 60)
    except Exception as e:
        print(f"Error saving message to cache: {e}")


def update_message_in_cache(message: ChatMessage) -> None:
    """
    Update an existing message in Redis cache.
    Args:
        message: ChatMessage instance to update.
    """
    cache_key = f"chat_messages_{message.room_id}"
    try:
        redis_client = cache.client.get_client()
        cached_messages = redis_client.lrange(cache_key, 0, -1)
        for i, cached_msg in enumerate(cached_messages):
            msg_data = json.loads(cached_msg)
            if msg_data["id"] == str(message.id):
                cache_data = {
                    "id": str(message.id),
                    "room_id": str(message.room_id),
                    "user_id": str(message.user_id),
                    "text": message.text,
                    "file_id": str(message.file_id) if message.file_id else None,
                    "replied_from_id": str(message.replied_from_id) if message.replied_from_id else None,
                    "is_delivered": message.is_delivered,
                    "is_read": message.is_read,
                    "is_deleted": message.is_deleted,
                    "is_system_message": message.is_system_message,
                    "read_at": int(message.read_at.timestamp()) if message.read_at else None,
                    "timestamp": int(message.timestamp.timestamp())
                }
                redis_client.lset(cache_key, i, json.dumps(cache_data, ensure_ascii=False))
                return
        # If message not found, save as new
        save_message_to_cache(message)
    except Exception as e:
        print(f"Error updating message in cache: {e}")


def delete_message_from_cache(message: ChatMessage) -> None:
    """
    Delete a message from Redis cache.
    Args:
        message: ChatMessage instance to delete.
    """
    cache_key = f"chat_messages_{message.room_id}"
    try:
        redis_client = cache.client.get_client()
        cached_messages = redis_client.lrange(cache_key, 0, -1)
        for cached_msg in cached_messages:
            msg_data = json.loads(cached_msg)
            if msg_data["id"] == str(message.id):
                redis_client.lrem(cache_key, 1, cached_msg)
                break
    except Exception as e:
        print(f"Error deleting message from cache: {e}")


def clear_room_cache(room_id: str) -> None:
    """
    Clear all cached messages for a given room.
    Args:
        room_id: ID of the chat room.
    """
    cache_key = f"chat_messages_{room_id}"
    try:
        cache.delete(cache_key)
    except Exception as e:
        print(f"Error clearing room cache: {e}")