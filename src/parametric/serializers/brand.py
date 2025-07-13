from rest_framework import serializers
from src.parametric.models import Brand


class InputBrandNameParametricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['title', 'fa_title', 'order',]


class OutPutBrandNameParametricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'title', 'fa_title',]