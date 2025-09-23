from rest_framework import serializers


class OutPutCompletedServiceItemSerializer(serializers.Serializer):
    description = serializers.CharField()
    cost = serializers.IntegerField()
    quantity = serializers.IntegerField()