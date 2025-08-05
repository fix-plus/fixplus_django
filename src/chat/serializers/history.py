from rest_framework import serializers
from src.authentication.models import User
from src.chat.models import ChatMessage

class OutputChatMessagesHistory(serializers.ModelSerializer):
    is_sent = serializers.SerializerMethodField()
    timestamp = serializers.SerializerMethodField()
    sender = serializers.SerializerMethodField()
    file_id = serializers.SerializerMethodField()
    replied_from_id = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = [
            'id',
            'is_sent',
            'text',
            'file_id',
            'replied_from_id',
            'is_system_message',
            'timestamp',
            'sender',
            'is_delivered',
            'is_read',
            'room_id',
        ]

    def get_is_sent(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            return str(obj.user_id) == str(request.user.id)
        return False

    def get_timestamp(self, obj):
        return int(obj.timestamp.timestamp())

    def get_sender(self, obj):
        if obj.is_system_message or self.get_is_sent(obj):
            return None
        try:
            user = User.objects.get(id=obj.user_id)
            full_name = user.get_full_name() or ''
            request = self.context.get('request')
            avatar = request.build_absolute_uri(user.profile.avatar.url) if hasattr(user, 'profile') and user.profile and user.profile.avatar else None
            return {
                'id': str(obj.user_id),
                'full_name': full_name,
                'avatar': avatar,
                'role': (
                    'TECHNICIAN' if user.groups.filter(name='TECHNICIAN').exists() else
                    'ADMIN' if user.groups.filter(name='ADMIN').exists() else
                    'SUPER_ADMIN' if user.groups.filter(name='SUPER_ADMIN').exists() else
                    'UNKNOWN'
                )
            }
        except User.DoesNotExist:
            return None

    def get_file_id(self, obj):
        return str(obj.file_id) if obj.file_id else None

    def get_replied_from_id(self, obj):
        return str(obj.replied_from_id) if obj.replied_from_id else None

class OutputUnReadMessagesCountSerializers(serializers.Serializer):
    service_id = serializers.UUIDField()
    unread_messages_count = serializers.IntegerField()
