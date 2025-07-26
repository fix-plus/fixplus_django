from rest_framework import serializers

from src.chat.models import ChatMessage


class OutputChatMessagesHistory(serializers.ModelSerializer):
    timestamp = serializers.SerializerMethodField()
    is_sent = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        exclude = ["user_id"]

    def get_timestamp(self, obj):
        return int(obj.timestamp.timestamp())

    def get_is_sent(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            return str(obj.user_id) == str(request.user.id)
        return False

class OutputUnReadMessagesCountSerializers(serializers.Serializer):
    service_id = serializers.UUIDField()
    unread_messages_count = serializers.IntegerField()
