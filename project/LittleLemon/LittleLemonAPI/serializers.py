from rest_framework import serializers
from django.contrib.auth.models import User,Group
from .models import MenuItem,Category

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']
        

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['title','price','featured','category']
        extra_kwargs = {
            'price':{'min_value': 2},
            'inventory': {'min_value': 0}
        }

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title']