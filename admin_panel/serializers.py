# serializers.py
from rest_framework import serializers
from .models import BaseFare

class BaseFareSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseFare
        fields = ['id','fare_type', 'amount']

