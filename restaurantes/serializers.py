from rest_framework_mongoengine import serializers
from .models import restaurants

class restaurantsSerializer(serializers.DocumentSerializer):
	class Meta:
		model = restaurants
		fields = ('restaurant_id', 'name', 'cuisine', 'borough', 'address', 'image', 'city')

class restaurantListSerializer(serializers.DocumentSerializer):
	class Meta:
		model = restaurants
		fields = ('restaurant_id', 'name')