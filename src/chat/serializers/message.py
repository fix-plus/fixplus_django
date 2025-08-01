from rest_framework import serializers

from src.authentication.models import User
from src.chat.models import ChatMessage


class OutputChatMessagesHistory(serializers.ModelSerializer):
    is_sent = serializers.SerializerMethodField()
    timestamp = serializers.SerializerMethodField()
    sender_id = serializers.SerializerMethodField()
    sender_role = serializers.SerializerMethodField()
    sender_full_name = serializers.SerializerMethodField()
    sender_avatar = serializers.SerializerMethodField()
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
            'sender_id',
            'sender_role',
            'sender_full_name',
            'sender_avatar',
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

    def get_sender_id(self, obj):
        if obj.is_system_message or self.get_is_sent(obj):
            return None
        return str(obj.user_id) if obj.user_id else None

    def get_sender_role(self, obj):
        if obj.is_system_message or self.get_is_sent(obj):
            return None
        try:
            user = User.objects.get(id=obj.user_id)
            return (
                'TECHNICIAN' if user.groups.filter(name='TECHNICIAN').exists() else
                'ADMIN' if user.groups.filter(name='ADMIN').exists() else
                'SUPER_ADMIN' if user.groups.filter(name='SUPER_ADMIN').exists() else
                'UNKNOWN'
            )
        except User.DoesNotExist:
            return 'UNKNOWN'

    def get_sender_full_name(self, obj):
        if obj.is_system_message or self.get_is_sent(obj):
            return None
        try:
            user = User.objects.get(id=obj.user_id)
            full_name = user.get_full_name() or ''
            if hasattr(user, 'profile') and user.profile and user.profile.full_name:
                full_name = user.profile.full_name
            return full_name
        except User.DoesNotExist:
            return ''

    def get_sender_avatar(self, obj):
        if obj.is_system_message or self.get_is_sent(obj):
            return None
        try:
            user = User.objects.get(id=obj.user_id)
            if hasattr(user, 'profile') and user.profile and user.profile.avatar:
                return str(user.profile.avatar.url)
            return None
        except User.DoesNotExist:
            return None

    def get_file_id(self, obj):
        return str(obj.file_id) if obj.file_id else None

    def get_replied_from_id(self, obj):
        return str(obj.replied_from_id) if obj.replied_from_id else None

class OutputUnReadMessagesCountSerializers(serializers.Serializer):
    service_id = serializers.UUIDField()
    unread_messages_count = serializers.IntegerField()
