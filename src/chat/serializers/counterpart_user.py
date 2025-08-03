from rest_framework import serializers
from src.chat.models.room import ChatRoom
from src.chat.models.member import ChatMembership


class InputParamsCounterpartUser(serializers.Serializer):
    role_list = serializers.CharField(default=None)
    full_name = serializers.CharField(default=None)


class OutputCounterpartUser(serializers.Serializer):
    id = serializers.CharField()
    full_name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    last_online = serializers.DateTimeField()
    room_id = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return obj.profile.full_name if hasattr(obj, 'profile') else None

    def get_avatar(self, obj):
        request = self.context.get('request')
        if hasattr(obj, 'profile') and obj.profile and obj.profile.avatar:
            return request.build_absolute_uri(obj.profile.avatar.url)

    def get_role(self, obj):
        return obj.get_role()

    def get_room_id(self, obj):
        request = self.context.get('request')
        if not request or not request.user:
            return None

        exclude_user_id = request.user.id
        queried_user_id = obj.id

        # Find rooms where both users are members
        user1_memberships = ChatMembership.objects.filter(
            user_id=exclude_user_id,
            left_at__isnull=True
        ).values_list('room_id', flat=True)

        user2_memberships = ChatMembership.objects.filter(
            user_id=queried_user_id,
            left_at__isnull=True
        ).values_list('room_id', flat=True)

        # Find common rooms (intersection of room_ids)
        common_room_ids = set(user1_memberships) & set(user2_memberships)

        # Filter for direct chat rooms (TECHNICIAN_DIRECT or ADMIN_DIRECT)
        common_room = ChatRoom.objects.filter(
            id__in=common_room_ids,
            type__in=[ChatRoom.Type.TECHNICIAN_DIRECT, ChatRoom.Type.ADMIN_DIRECT]
        ).first()

        return str(common_room.id) if common_room else None