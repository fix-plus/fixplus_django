from rest_framework import serializers

from src.media.serializers import OutputMediaSerializer
from src.account.models import TechnicianServiceCard
from src.parametric.serializers.brand import OutPutBrandNameParametricSerializer


class OutputTechnicianOwnServiceCardSerializer(serializers.ModelSerializer):
    brand = OutPutBrandNameParametricSerializer()
    photo = OutputMediaSerializer()

    class Meta:
        model = TechnicianServiceCard
        fields = ['id', 'brand', 'photo']
