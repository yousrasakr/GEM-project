from rest_framework import serializers
from .models import Statue

class StatueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statue
        fields = '__all__'  # include all model fields
