from rest_framework import serializers
from App.models import Category, CustomUser, Product
from django.contrib.auth.hashers import check_password, make_password
from rest_framework import status



class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password','email')

    def create(self, data):
        try:    
            username = data['username']
            email = data['email']
            password = data['password']
            hashedpassword = make_password(password) 
            user= CustomUser.objects.create(
                username = username,
                email = email,
                password = hashedpassword
            )
            return user
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField()  
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'created_at', 'updated_at']

    def create(self, validate_data):
        product = Product.objects.create(
            name=validate_data['name'],
            description=validate_data['description'],
            price=validate_data['price'], 
            category=validate_data['category'],
        )
        return product
