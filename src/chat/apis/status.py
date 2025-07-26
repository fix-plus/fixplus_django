# from drf_spectacular.utils import extend_schema
# from rest_framework.response import Response
# from rest_framework.views import APIView
#
# from src.chat.selectors.api import calculate_unread_messages
# from src.chat.serializers.message import OutputChatMessagesHistory, OutputUnReadMessagesCountSerializers
# from src.common.mixins import IsVerifiedMixin
#
#
# class UnReadChatMessagesCountApi(IsVerifiedMixin, APIView):
#     @extend_schema(
#         summary="Get Unread Chat Messages Count",
#         responses=OutputUnReadMessagesCountSerializers,
#     )
#     def get(self, request, deal_offer_id):
#         # Initialize
#         user = request.user
#
#         # Queryset
#         queryset = calculate_unread_messages(
#             user=user,
#             deal_offer_id=deal_offer_id,
#         )
#
#         # Response
#         return Response(OutputUnReadMessagesCountSerializers(queryset).data)