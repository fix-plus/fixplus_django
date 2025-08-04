from rest_framework import serializers
from src.chat.models import ChatRoom

class InputParamsChatRoomSerializer(serializers.Serializer):
    room_type = serializers.ChoiceField(
        choices=ChatRoom.Type.choices,
        required=False,
        allow_null=True
    )
    search = serializers.CharField(max_length=200, required=False, allow_blank=True)

class SenderSerializer(serializers.Serializer):
    full_name = serializers.CharField(allow_null=True)
    avatar = serializers.SerializerMethodField()
    role = serializers.CharField(allow_null=True)

    def get_avatar(self, obj):
        request = self.context.get('request')
        if obj.get('avatar'):
            return request.build_absolute_uri(obj.get('avatar').url) if request else obj.get('avatar').url
        return None

class LastMessageSerializer(serializers.Serializer):
    message_id = serializers.UUIDField()
    text = serializers.CharField(allow_null=True)
    timestamp = serializers.DateTimeField()
    is_sent = serializers.BooleanField()
    is_system_message = serializers.BooleanField()
    sender = SenderSerializer(allow_null=True)

class CounterpartSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    full_name = serializers.CharField(allow_null=True)
    avatar = serializers.SerializerMethodField()
    role = serializers.CharField(allow_null=True)

    def get_avatar(self, obj):
        request = self.context.get('request')
        if obj.get('avatar'):
            return request.build_absolute_uri(obj.get('avatar').url) if request else obj.get('avatar').url
        return None

class ServiceSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    created_at = serializers.DateTimeField()
    status = serializers.CharField()

class CustomerSerializer(serializers.Serializer):
    full_name = serializers.CharField(allow_null=True)
    phone_number = serializers.CharField(allow_null=True)
    address = serializers.CharField(allow_null=True)

class OutputChatRoomSerializer(serializers.Serializer):
    room_id = serializers.UUIDField()
    type = serializers.CharField()
    unread_messages_count = serializers.IntegerField()
    last_message = LastMessageSerializer(allow_null=True)
    counterpart = CounterpartSerializer(allow_null=True)
    service = ServiceSerializer(allow_null=True)
    customer = CustomerSerializer(allow_null=True)