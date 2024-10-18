from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from App.models import Category, CustomUser, Product
from .serializers import CategorySerializer, ProductSerializer, UserRegistrationSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError as JWTTokenError, AuthenticationFailed
from django.contrib.auth import authenticate
from rest_framework.pagination import PageNumberPagination


'''
    USER REGISTERATION API(USER SHOULD REGISTER WITH EMAIL , USERNAME AND PASSWORD)
'''
class UserRegistrationApiView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        datas = request.data
        serializer = UserRegistrationSerializer(data = datas)
        if serializer.is_valid():
            serializer.save()
            return Response ({'message': 'Registration Sucessfull'}, status = status.HTTP_200_OK)  
        return Response({'error': serializer.errors}, status= status.HTTP_400_BAD_REQUEST)  



'''
    User can Login using respective email and password
'''

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"detail": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed("Invalid email or password.")

        if not user.check_password(password):
            raise AuthenticationFailed("Invalid email or password.")
        
        if not user.is_active:
            raise AuthenticationFailed("User account is not active.")
        
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'email': user.email,
        }, status=status.HTTP_200_OK)





'''
    THIS API WILL PROVIDE REFRESH TOKEN FOR SECURITY
'''
class RefreshTokenApiview(APIView):
    
    def get (self, request):

        refresh_token = request.GET.get('refresh')

        if not refresh_token:
            return Response({'error': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = refresh.access_token

            return Response({
                'access': str(new_access_token),
            }, status=status.HTTP_200_OK)

        except JWTTokenError as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)


'''
     This api can able to fetch the datas from category table and post the data
'''

class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size' 


class CategoryListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):

        categories = Category.objects.all()

        pagination = StandardPagination() 
        
        Pagination_data = pagination.paginate_queryset(categories, request)

        serializer = CategorySerializer(Pagination_data, many=True)

        paginated_response = {
            'count': pagination.page.paginator.count, 
            'num_pages': pagination.page.paginator.num_pages, 
            'current_page': pagination.page.number,  
            'next': pagination.get_next_link(),  
            'previous': pagination.get_previous_link(),
            'results': serializer.data  
        }
        
        return Response(paginated_response, status= status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response( { 'message' : 'Data Saved Successfully', 'data' : serializer.data } , status=status.HTTP_201_CREATED )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


'''
     This api can retrieve the specific data
'''
class CategoryDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        value = request.data.get('pk')
        category = get_object_or_404(Category, pk=value)
        serializer = CategorySerializer(category)
        return Response(serializer.data)



'''
        PRODUCT GET AND CREATE API
'''

class ProductListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        name = request.GET.get('name', None)
        category_id = request.GET.get('category', None)

 
        products = Product.objects.all()

    
        if name:
            products = products.filter(name__icontains=name)  

 
        if category_id:
            products = products.filter(category_id=category_id)
        
        pagination = StandardPagination() 
        
        Pagination_data = pagination.paginate_queryset(products, request)

        serializer = ProductSerializer(Pagination_data, many=True)

        paginated_response = pagination.get_paginated_response(serializer.data)

        paginated_response.status_code = status.HTTP_200_OK

        return (paginated_response)



    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProductDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
