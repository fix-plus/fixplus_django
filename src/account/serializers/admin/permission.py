from rest_framework import serializers
from django.contrib.auth.models import Permission


class OutPutPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'codename', 'name']
