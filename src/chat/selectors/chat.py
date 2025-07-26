from uuid import UUID
from typing import List, Optional
from django.db.models import Q
from src.authentication.models import User
from src.chat.models import ChatRoom, ChatMembership, ChatMessage
from src.chat.selectors.message import calculate_unread_messages
from src.customer.models import CustomerContactNumber
from src.service.models import Service


def get_chat_room_list(
        *,
        user: User,
        room_type: Optional[str] = None,
        search: Optional[str] = None
) -> List[dict]:
    """
    Retrieve a list of chat rooms (SERVICE, TECHNICIAN_DIRECT, ADMIN_DIRECT) for the given user.
    Supports filtering by room type and searching by customer full_name (for SERVICE) or member full_name (for DIRECT).
    Args:
        user: The authenticated user.
        room_type: Optional room type to filter (SERVICE, TECHNICIAN_DIRECT, ADMIN_DIRECT).
        search: Optional search term for customer full_name (SERVICE) or member full_name (DIRECT).
    Returns:
        List of dictionaries containing room details, unread message counts, last message,
        sender information, and service/customer details.
    """
    # Get active memberships for the user
    memberships = ChatMembership.objects.filter(
        user_id=user.id,
        left_at__isnull=True
    ).values_list('room_id', flat=True)

    # Base query for rooms where the user is an active member
    rooms_query = ChatRoom.objects.filter(id__in=memberships)

    # Filter by room type if provided
    if room_type:
        valid_types = [
            ChatRoom.Type.SERVICE,
            ChatRoom.Type.TECHNICIAN_DIRECT,
            ChatRoom.Type.ADMIN_DIRECT
        ]
        if room_type not in valid_types:
            return []
        rooms_query = rooms_query.filter(type=room_type)
    else:
        rooms_query = rooms_query.filter(
            type__in=[
                ChatRoom.Type.SERVICE,
                ChatRoom.Type.TECHNICIAN_DIRECT,
                ChatRoom.Type.ADMIN_DIRECT
            ]
        )

    # Apply search filter
    if search:
        search = search.strip()
        if room_type == ChatRoom.Type.SERVICE:
            # Search by customer full_name for SERVICE rooms
            service_ids = Service.objects.filter(
                customer__full_name__icontains=search
            ).exclude(customer__full_name__isnull=True).values_list('id', flat=True)
            rooms_query = rooms_query.filter(service_id__in=list(service_ids))
        elif room_type in [ChatRoom.Type.TECHNICIAN_DIRECT, ChatRoom.Type.ADMIN_DIRECT]:
            # Search by other member's full_name for DIRECT rooms
            matching_memberships = ChatMembership.objects.filter(
                room_id__in=rooms_query.values_list('id', flat=True),
                left_at__isnull=True
            ).exclude(user_id=user.id).select_related('user__profile')
            matching_room_ids = []
            for membership in matching_memberships:
                full_name = (
                    membership.user.profile.full_name
                    if hasattr(membership.user, 'profile') and membership.user.profile.full_name
                    else membership.user.get_full_name() or ''
                )
                if search.lower() in full_name.lower():
                    matching_room_ids.append(membership.room_id)
            rooms_query = rooms_query.filter(id__in=matching_room_ids)

    result = []
    for room in rooms_query:
        # Calculate unread messages for the room
        unread_count = calculate_unread_messages(room_id=str(room.id), user_id=str(user.id))

        # Get the last message for the room
        last_message = ChatMessage.objects.filter(room_id=room.id).order_by('-timestamp').first()
        last_message_data = None
        last_message_date = None
        sender_data = None

        if last_message:
            last_message_date = last_message.timestamp.isoformat()
            last_message_data = {
                'message_id': str(last_message.id),
                'text': last_message.text,
                'timestamp': last_message_date,
                'is_sent': str(last_message.user_id) == str(user.id) if last_message.user_id else False,
                'is_system_message': last_message.is_system_message
            }

            # Get sender's details
            if last_message.user_id and not last_message.is_system_message:
                try:
                    sender = User.objects.get(id=last_message.user_id)
                    sender_data = {
                        'full_name': sender.profile.full_name if hasattr(sender,
                                                                         'profile') else sender.get_full_name() or '',
                        'role': (
                            'TECHNICIAN' if sender.groups.filter(name='TECHNICIAN').exists() else
                            'ADMIN' if sender.groups.filter(name='ADMIN').exists() else
                            'SUPER_ADMIN' if sender.groups.filter(name='SUPER_ADMIN').exists() else
                            'UNKNOWN'
                        )
                    }
                except User.DoesNotExist:
                    sender_data = {'full_name': '', 'role': 'UNKNOWN'}

        # Prepare room details
        room_data = {
            'room_id': str(room.id),
            'type': room.type,
            'service_id': str(room.service_id) if room.service_id else None,
            'unread_messages_count': unread_count,
            'members': [],
            'last_message': last_message_data,
            'last_message_date': last_message_date,
            'sender': sender_data,
            'service': None,
            'customer': None
        }

        # Add service-specific details for SERVICE rooms
        if room.type == ChatRoom.Type.SERVICE and room.service_id:
            try:
                service = Service.objects.get(id=room.service_id)
                # Service details
                room_data['service'] = {
                    'created_at': service.created_at.isoformat(),
                    'status': service.status
                }

                # Customer details
                customer = service.customer
                primary_contact = CustomerContactNumber.objects.filter(
                    customer=customer,
                    is_primary=True
                ).first()

                room_data['customer'] = {
                    'full_name': customer.full_name or '',
                    'phone_number': primary_contact.number if primary_contact else None,
                    'address': str(service.address) if service.address else None
                }

            except Service.DoesNotExist:
                # Handle case where service is not found
                pass

        # For direct rooms, include member details
        if room.type in [ChatRoom.Type.TECHNICIAN_DIRECT, ChatRoom.Type.ADMIN_DIRECT]:
            members = ChatMembership.objects.filter(
                room_id=room.id,
                left_at__isnull=True
            ).select_related('user__profile')
            room_data['members'] = [
                {
                    'user_id': str(membership.user_id),
                    'full_name': membership.user.profile.full_name if hasattr(membership.user,
                                                                              'profile') else membership.user.get_full_name() or '',
                    'avatar': str(membership.user.profile.avatar.url) if hasattr(membership.user,
                                                                                 'profile') and membership.user.profile.avatar else None
                } for membership in members if str(membership.user_id) != str(user.id)
            ]

        result.append(room_data)

    return result