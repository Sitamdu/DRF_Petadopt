from rest_framework import serializers
from .models import *

class PetSerializer(serializers.ModelSerializer):
    #adding custom field
    len_name = serializers.SerializerMethodField()
    class Meta:
        model = Pet
        fields = '__all__'


    def get_len_name(self, object):
        length = len(object.name)
        return length


    def validate(self, data):
        if data['name'] == data['species']:
            raise serializers.ValidationError("Name and species cant be same!")
        else:
            return data

    def validated_name(self, value):
        if len(value) > 2:
            raise serializers.ValidationError("Name is too short!")
        else:
            return value


class AdoptSerializer(serializers.ModelSerializer):
    adoption_requests = PetSerializer(many=True, read_only=True)

    class Meta:
        model = AdoptionRequest
        fields = '__all__'




class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'



