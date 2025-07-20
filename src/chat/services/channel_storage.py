from django.core.cache import cache
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class ChannelStorage:
    """
    Service for managing WebSocket channel names using Django's cache framework.
    Stores channel names for online users and provides methods to store, retrieve, and remove them.
    """
    def __init__(self):
        self.cache = cache

    def store_channel_name(self, user_id: str, channel_name: str) -> None:
        """
        Store a user's channel name in the cache.
        Args:
            user_id: ID of the user.
            channel_name: WebSocket channel name to store.
        """
        try:
            key = f"channel:user:{user_id}"
            self.cache.set(key, channel_name)
            logger.info(f"Stored channel name {channel_name} for user {user_id} in cache")
        except Exception as e:
            logger.error(f"Failed to store channel name for user {user_id}: {str(e)}")

    def remove_channel_name(self, user_id: str) -> None:
        """
        Remove a user's channel name from the cache.
        Args:
            user_id: ID of the user.
        """
        try:
            key = f"channel:user:{user_id}"
            self.cache.delete(key)
            logger.info(f"Removed channel name for user {user_id} from cache")
        except Exception as e:
            logger.error(f"Failed to remove channel name for user {user_id}: {str(e)}")

    def get_channel_name(self, user_id: str) -> Optional[str]:
        """
        Retrieve a user's channel name from the cache.
        Args:
            user_id: ID of the user.
        Returns:
            The channel name if found, else None.
        """
        try:
            key = f"channel:user:{user_id}"
            channel_name = self.cache.get(key)
            if channel_name:
                logger.debug(f"Retrieved channel name {channel_name} for user {user_id} from cache")
            else:
                logger.debug(f"No channel name found for user {user_id} in cache")
            return channel_name
        except Exception as e:
            logger.error(f"Failed to retrieve channel name for user {user_id}: {str(e)}")
            return None

channel_storage = ChannelStorage()