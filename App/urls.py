from django.urls import path
from App.apis.apis import (
    CategoryListCreateAPIView,
    CategoryDetailAPIView,
    LoginAPIView,
    ProductListCreateAPIView,
    ProductDetailAPIView,
    RefreshTokenApiview,
    UserRegistrationApiView
)

urlpatterns = [
    #Register Api
    path('register/', UserRegistrationApiView.as_view(), name='register'),

    #Login APis
    path('login/', LoginAPIView.as_view(), name='login'),
    path('token/refresh/', RefreshTokenApiview.as_view(), name='token_refresh'),

    # Categories API
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categoriesretrieve/', CategoryDetailAPIView.as_view(), name='category-detail'),

    # Products API
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
]
