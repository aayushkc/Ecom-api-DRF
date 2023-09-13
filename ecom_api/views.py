from django.shortcuts import render
from django.contrib.auth import login
from django.http import Http404, HttpResponseNotAllowed
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import RegisterSerializer, MyTokenObtainPairSerializer, ProductSerializer, OrderSerializer
from .models import MyUser, Product, Order
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from .permissions import IsSeller,IsBuyer


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterUser(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        
class GetUser:
    """
    Get the user from the requested email
    """
    def get_user(self, user):
        curr_user = MyUser.objects.get(email= user)
        return curr_user 
    

class SellerProduct(APIView, PageNumberPagination):
    permission_classes = [IsAuthenticated, IsSeller]
    def post(self ,request):
        """
        Allows ony seller account to post products
        """
        print(request.data)
        if request.user.id == request.data['seller']:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
       
    def get(self, request):
        """
        Lists all the items for the specific seller account
        """
        user = GetUser.get_user(GetUser, request.user)
        userProduts = Product.objects.filter(seller=user).order_by('id')
        name = request.query_params.get('name')
        if name is not None:
            userProduts = userProduts.filter(name=name)
        result_page = self.paginate_queryset(userProduts, request, view=self)
        serializer = ProductSerializer(result_page, many= True)
        return self.get_paginated_response(serializer.data)

        
class IndividualProduct(APIView):
    def get(self, request,id):
        try:
            user = GetUser.get_user(GetUser,request.user)
        except:
            user = None
        if user:
            if user.is_seller:
                """
                Lists porduct releated to the seller account only
                Limits seller accounts to view their products
                """
                try:
                    products = Product.objects.get(id=id, seller=user)
                    serializer = ProductSerializer(products)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except :
                    return Response(status=status.HTTP_204_NO_CONTENT )
            else:
                """
                List product detail for any account
                Allows buyers accounts to access any product-details
                """
                try:
                    products = Product.objects.get(id=id)
                    serializer = ProductSerializer(products)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except :
                    return Response(status=status.HTTP_204_NO_CONTENT )
        else:

            """"
            Allows anonymous user to view any product-details
            """
            products = Product.objects.get(id=id)
            serializer = ProductSerializer(products)
            try:
                return Response(serializer.data, status=status.HTTP_200_OK)
            except :
                raise Http404
        
    def put(self, request, id):
        try:
            user = GetUser.get_user(GetUser,request.user)
        except:
           raise HttpResponseNotAllowed
       
        if user.is_seller:
                
                """"
                Allows Only seller account can update products
                """
                try:
                    products = Product.objects.get(id=id, seller=user)
                    serializer = ProductSerializer(products, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except :
                    return Response(status=status.HTTP_204_NO_CONTENT )
       
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
    def delete(self, request, id):
        try:
            user = GetUser.get_user(GetUser,request.user)
        except:
           raise HttpResponseNotAllowed
       
        if user.is_seller:
                
                """"
                Allows Only seller account can delete products
                """
                try:
                    products = Product.objects.get(id=id, seller=user)
                    products.delete()  
                    return Response(status=status.HTTP_204_NO_CONTENT)
                except:
                    return Response(status=status.HTTP_204_NO_CONTENT)
       
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
class ListProduct(APIView, PageNumberPagination):
    """
    Any kind of user can view all the products
    """
    def get(self, request):
        products = Product.objects.all()
        result_page = self.paginate_queryset(products, request, view=self)
        serializer = ProductSerializer(result_page, many = True)
        return self.get_paginated_response(serializer.data)
    

class OrderProduct(APIView, PageNumberPagination):
    """
    Only for buyers account
    Allows to get the products ordered by the buyer
    Allows to create a order for the given buyer account
    """
    permission_classes=[IsAuthenticated, IsBuyer]
    def get(self, request):
        self.check_object_permissions(request, OrderProduct)
        user = GetUser().get_user(request.user)
        orders = Order.objects.filter(buyer=user)
        result_page = self.paginate_queryset(orders, request, view=self)
        serializer = OrderSerializer(result_page, many= True)
        return self.get_paginated_response(serializer.data)
       
    
    def post(self, request):
        self.check_object_permissions(request, OrderProduct)
        user = GetUser().get_user(request.user)
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
class ListOrder(APIView, PageNumberPagination):
     """
     Only for seller account
     Lists all the product of seller ordered by buyer account
     """
     permission_classes=[IsAuthenticated, IsSeller]
     
     def get(self, request):
        self.check_object_permissions(request, ListOrder)
        user = GetUser().get_user(request.user)
        products = Product.objects.filter(seller= user)
        orders = Order.objects.filter(product__in=products, status=False)
        result_page = self.paginate_queryset(orders, request, view=self)
        serializer = OrderSerializer(result_page, many= True)
        return self.get_paginated_response(serializer.data)
       
class BuyerChangeOrder(APIView):
    """
    Only Buers can perform following actions:
    1) Edit placed order
    2) Delete placed order
    """
    permission_classes = [IsAuthenticated, IsBuyer]
    def put(self, request, id):
        self.check_object_permissions(request, ListOrder)
        user = GetUser().get_user(request.user)
        try:
            order = Order.objects.get(id=id,status=False, buyer=user)
        except:
            raise Http404
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, id):
        self.check_object_permissions(request, ListOrder)
        user = GetUser().get_user(request.user)
        try:
            order = Order.objects.get(id=id, buyer = user)
        except:
            raise Http404
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SellerChangeOrder(APIView):
    """
    Only Seller can perform following actions:
    1) Edit placed order
    """
    permission_classes = [IsAuthenticated, IsSeller]
    def put(self, request, id):
            self.check_object_permissions(request, ListOrder)
            try:
                order = Order.objects.get(id=id,status=False)
            except:
                raise Http404
            serializer = OrderSerializer(order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
class TotalRevenue(APIView):
    """
    Only Seller can perform following actions:
    1) Get the total revenue
    """
    permission_classes = [IsAuthenticated, IsSeller]
    def get(self, request):
            self.check_object_permissions(request, ListOrder)
            prodcuts = Product.objects.filter(seller = request.user)
            orders = Order.objects.filter(product__in=prodcuts, status = True)
            price = 0
            for order in orders:
                price += order.product.price
                
            return Response(price, status=status.HTTP_200_OK)
    