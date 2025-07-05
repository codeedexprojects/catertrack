# serializers.py
from rest_framework import serializers
from admin_panel.models import *

class BaseFareSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseFare
        fields = ['id','fare_type', 'amount']

class BoyRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoyRating
        fields = [
            'id', 'user', 'pant', 'shoe', 'timing', 'neatness', 'performance',
            'comment', 'rated_by', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'rated_by']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['rated_by'] = request.user
        return super().create(validated_data)
    
class BoyRatingPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoyRating
        fields = [
            'id', 'pant', 'shoe', 'timing', 'neatness', 'performance', 'comment'
        ]
        read_only_fields = ['id']

class DailyWageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyWage
        fields = [
            'id', 'user', 'date',
            'base_fare', 'rating_amount',
            'travel_allowance', 'over_time',
            'long_fare', 'bonus', 'total_wage'
        ]
        read_only_fields = ['id', 'total_wage']

    def create(self, validated_data):
        instance = DailyWage.objects.create(**validated_data)
        instance.total_wage = instance.calculate_total()
        instance.save()
        return instance

class DailyWagePatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyWage
        fields = [
            'id', 'travel_allowance', 'over_time', 'long_fare', 'bonus', 'total_wage'
        ]
        read_only_fields = ['id', 'total_wage']

    def update(self, instance, validated_data):
        instance.travel_allowance = validated_data.get('travel_allowance', instance.travel_allowance)
        instance.over_time = validated_data.get('over_time', instance.over_time)
        instance.long_fare = validated_data.get('long_fare', instance.long_fare)
        instance.bonus = validated_data.get('bonus', instance.bonus)

        instance.total_wage = instance.calculate_total()
        instance.save()
        return instance
    
class CateringWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CateringWork
        fields = [
            'id', 'customer_name', 'customer_mobile',
            'address', 'place', 'district',
            'date', 'time', 'work_type', 'status',
            'no_of_boys_needed', 'attendees',
            'assigned_supervisor', 'assigned_boys',
            'remarks', 'payment_amount', 'location_url',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']