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
    print(f"Memberships: {list(memberships)}")

    # Base query for rooms where the user is an active member
    rooms_query = ChatRoom.objects.filter(id__in=memberships)
    print(f"Initial rooms: {list(rooms_query.values('id', 'type', 'service_id'))}")

    # Filter by room type if provided
    if room_type:
        valid_types = [
            ChatRoom.Type.SERVICE,
            ChatRoom.Type.TECHNICIAN_DIRECT,
            ChatRoom.Type.ADMIN_DIRECT
        ]
        if room_type not in valid_types:
            print(f"Invalid room_type: {room_type}")
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
    print(f"Rooms after type filter: {list(rooms_query.values('id', 'type', 'service_id'))}")

    # Apply search filter
    if search:
        search = search.strip()
        print(f"Search term: {search}")
        if room_type == ChatRoom.Type.SERVICE:
            # Search by customer full_name for SERVICE rooms
            service_ids = Service.objects.filter(
                customer__full_name__icontains=search
            ).exclude(customer__full_name__isnull=True).values_list('id', flat=True)
            service_ids = [str(service_id) for service_id in service_ids]
            print(f"Service IDs: {list(service_ids)}")
            rooms_query = rooms_query.filter(service_id__in=service_ids)
            print(f"Rooms after search filter: {list(rooms_query.values('id', 'type', 'service_id'))}")
        elif room_type in [ChatRoom.Type.TECHNICIAN_DIRECT, ChatRoom.Type.ADMIN_DIRECT]:
            # Search by other member's full_name for DIRECT rooms
            matching_memberships = ChatMembership.objects.filter(
                room_id__in=rooms_query.values_list('id', flat=True),
                left_at__isnull=True
            ).exclude(user_id=user.id)
            matching_room_ids = []
            for membership in matching_memberships:
                try:
                    member_user = User.objects.get(id=membership.user_id)
                    full_name = member_user.get_full_name() or ''
                    if hasattr(member_user, 'profile') and member_user.profile and member_user.profile.full_name:
                        full_name = member_user.profile.full_name
                    print(f"Checking member {membership.user_id}: full_name={full_name}")
                    if search.lower() in full_name.lower():
                        matching_room_ids.append(membership.room_id)
                except User.DoesNotExist:
                    print(f"User {membership.user_id} not found")
                    continue
            print(f"Matching room IDs for direct: {matching_room_ids}")
            rooms_query = rooms_query.filter(id__in=matching_room_ids)
            print(f"Rooms after search filter: {list(rooms_query.values('id', 'type'))}")

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
            last_message_date = last_message.timestamp
            last_message_data = {
                'message_id': str(last_message.id),
                'text': last_message.text,
                'timestamp': last_message_date,
                'is_sent': str(last_message.user_id) == str(user.id) if last_message.user_id else False,
                'is_system_message': last_message.is_system_message,
                'sender': None
            }

            # Get sender's details for last message
            if last_message.user_id and not last_message.is_system_message:
                try:
                    sender = User.objects.get(id=last_message.user_id)
                    full_name = sender.get_full_name() or ''
                    if hasattr(sender, 'profile') and sender.profile and sender.profile.full_name:
                        full_name = sender.profile.full_name
                    avatar = sender.profile.avatar if hasattr(sender, 'profile') and sender.profile and sender.profile.avatar else None
                    sender_data = {
                        'full_name': full_name,
                        'avatar': avatar,
                        'role': (
                            'TECHNICIAN' if sender.groups.filter(name='TECHNICIAN').exists() else
                            'ADMIN' if sender.groups.filter(name='ADMIN').exists() else
                            'SUPER_ADMIN' if sender.groups.filter(name='SUPER_ADMIN').exists() else
                            'UNKNOWN'
                        )
                    }
                    last_message_data['sender'] = sender_data
                except User.DoesNotExist:
                    last_message_data['sender'] = {'full_name': '', 'role': 'UNKNOWN', 'avatar': None}

        # Prepare room details
        room_data = {
            'room_id': str(room.id),
            'type': room.type,
            'unread_messages_count': unread_count,
            'last_message': last_message_data,
            'last_message_date': last_message_date,
            'counterpart': None,
            'service': None,
            'customer': None
        }

        # Add service-specific details for SERVICE rooms
        if room.type == ChatRoom.Type.SERVICE and room.service_id:
            try:
                service = Service.objects.get(id=room.service_id)
                # Service details
                room_data['service'] = {
                    'id': str(room.service_id),
                    'created_at': service.created_at,
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
                print(f"Service {room.service_id} not found")
                pass

        # Add counterpart details for DIRECT rooms
        if room.type in [ChatRoom.Type.TECHNICIAN_DIRECT, ChatRoom.Type.ADMIN_DIRECT]:
            members = ChatMembership.objects.filter(
                room_id=room.id,
                left_at__isnull=True
            ).exclude(user_id=user.id)
            if members.exists():
                membership = members.first()
                try:
                    counterpart_user = User.objects.get(id=membership.user_id)
                    full_name = counterpart_user.get_full_name() or ''
                    if hasattr(counterpart_user, 'profile') and counterpart_user.profile and counterpart_user.profile.full_name:
                        full_name = counterpart_user.profile.full_name
                    avatar = counterpart_user.profile.avatar if hasattr(counterpart_user, 'profile') and counterpart_user.profile and counterpart_user.profile.avatar else None
                    room_data['counterpart'] = {
                        'user_id': str(membership.user_id),
                        'full_name': full_name,
                        'avatar': avatar,
                        'role': (
                            'TECHNICIAN' if counterpart_user.groups.filter(name='TECHNICIAN').exists() else
                            'ADMIN' if counterpart_user.groups.filter(name='ADMIN').exists() else
                            'SUPER_ADMIN' if counterpart_user.groups.filter(name='SUPER_ADMIN').exists() else
                            'UNKNOWN'
                        )
                    }
                except User.DoesNotExist:
                    print(f"User {membership.user_id} not found")
                    room_data['counterpart'] = None

        result.append(room_data)

    return result