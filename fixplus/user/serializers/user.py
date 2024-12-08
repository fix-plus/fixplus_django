# users/serializers/users.py

from rest_framework import serializers
from django.contrib.auth.models import Group

from fixplus.user.models import BaseUser


class InputUserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Group.objects.all(),
        required=False
    )

    class Meta:
        model = BaseUser
        fields = ['id', 'mobile', 'is_active', 'status', 'reason_for_rejected', 'groups']

    def create(self, validated_data):
        groups = validated_data.pop('groups', [])
        user = BaseUser.objects.create_user(**validated_data)
        user.groups.set(groups)
        return user

    def update(self, instance, validated_data):
        groups = validated_data.pop('groups', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if groups is not None:
            instance.groups.set(groups)

        return instance


class OutPutUserSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True)

    class Meta:
        model = BaseUser
        fields = ['id', 'mobile', 'is_active', 'status', 'reason_for_rejected', 'groups']
