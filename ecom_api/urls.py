from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterUser, MyObtainTokenPairView, SellerProduct, IndividualProduct, ListProduct, OrderProduct, ListOrder, BuyerChangeOrder, SellerChangeOrder,TotalRevenue
urlpatterns = [
    path('register', view = RegisterUser.as_view(), name='registerUser'),
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('products', SellerProduct.as_view(), name='poduct'),
    path('product-details/<int:id>', IndividualProduct.as_view(), name='indiPro'),
    path('list-products', ListProduct.as_view(), name='list-all-products'),

    path('list-orders', ListOrder.as_view(), name='list-all-orders'),
    path('order', OrderProduct.as_view(), name='order'),
    path('change-order/<int:id>', BuyerChangeOrder.as_view(), name='change-order'),
    path('change-order-seller/<int:id>', SellerChangeOrder.as_view(), name='change--seller-order'),
    path('total-revenue', TotalRevenue.as_view(), name='total-revenue'),
]