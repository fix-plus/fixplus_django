from rest_framework import serializers

from src.chat.models import ChatRoom


class InputParamsChatRoomSerializer(serializers.Serializer):
    room_type = serializers.ChoiceField(
        choices=ChatRoom.Type.choices,
        required=False,
        allow_null=True
    )
    search = serializers.CharField(max_length=200, required=False, allow_blank=True)

class LastMessageSerializer(serializers.Serializer):
    message_id = serializers.UUIDField()
    text = serializers.CharField(allow_null=True)
    timestamp = serializers.DateTimeField()
    is_sent = serializers.BooleanField()
    is_system_message = serializers.BooleanField()

class SenderSerializer(serializers.Serializer):
    full_name = serializers.CharField(allow_null=True)
    role = serializers.CharField(allow_null=True)

class ServiceSerializer(serializers.Serializer):
    created_at = serializers.DateTimeField()
    status = serializers.CharField()

class CustomerSerializer(serializers.Serializer):
    full_name = serializers.CharField(allow_null=True)
    phone_number = serializers.CharField(allow_null=True)
    address = serializers.CharField(allow_null=True)

class OutputChatRoomSerializer(serializers.Serializer):
    room_id = serializers.UUIDField()
    type = serializers.CharField()
    service_id = serializers.UUIDField(allow_null=True)
    unread_messages_count = serializers.IntegerField()
    last_message = LastMessageSerializer(allow_null=True)
    last_message_date = serializers.DateTimeField(allow_null=True)
    sender = SenderSerializer(allow_null=True)
    service = ServiceSerializer(allow_null=True)
    customer = CustomerSerializer(allow_null=True)

