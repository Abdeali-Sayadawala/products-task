from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Category, Product
from customers.models import Customer
from .forms import ProductFrom, CategoryFrom
from .serializers import CategorySerializer, ProductSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status, generics
import datetime

# Create your views here
@api_view(['GET', 'POST', 'PUT'])
@permission_classes([AllowAny])
def get_products(request):

    return Response(data={"msg": "success"}, status=status.HTTP_200_OK)

class CategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        queryset = Category.objects.all()
        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        
        sub_category = self.request.query_params.get('sub_category')
        if sub_category is not None:
            queryset = queryset.filter(sub_category=Category.objects.get(id=int(sub_category)))
        return queryset

class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        queryset = Product.objects.all()
        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        
        price = self.request.query_params.get('price')
        if price is not None:
            queryset = queryset.filter(price=price)
        
        status = self.request.query_params.get('status')
        if status is not None:
            queryset = queryset.filter(status=status)
        
        product_code = self.request.query_params.get('product_code')
        if product_code is not None:
            queryset = queryset.filter(product_code__icontains=product_code)
        
        sub_category = self.request.query_params.get('sub_category')
        if sub_category is not None:
            queryset = queryset.filter(sub_category=Category.objects.get(id=int(sub_category)))

        manufacture_date = self.request.query_params.get('manufacture_date')
        if manufacture_date is not None:
            queryset = queryset.filter(manufacture_date=datetime.datetime.strptime(manufacture_date, "%Y-%m-%d").date())
        
        expiry_date = self.request.query_params.get('expiry_date')
        if expiry_date is not None:
            queryset = queryset.filter(expiry_date=datetime.datetime.strptime(expiry_date, "%Y-%m-%d").date())
        return queryset

@api_view(['GET', 'POST', 'PUT'])
@permission_classes([AllowAny])
def products(request):
    #checking login
    if 'email' not in request.session:
        # return render(request, "login.html", context={"error": "Login First!"})
        return redirect('/login/')
    if request.method == "GET":
        categories = Category.objects.all()
        product_form = ProductFrom
        category_form = CategoryFrom
        products = Product.objects.all()
        user = Customer.objects.get(id=request.session['id'])
        return render(request, "products.html", context={"categories": categories, "form": product_form, "category_form": category_form, "products": products, 'user': user})

    if request.method == "POST":
        print(request.data)
        if request.data['type'] == "category":
            request.data.customer = request.session['id']
            form = CategoryFrom(request.data)
            if form.is_valid():
                form.save()
                category_obj = form.instance
                category_obj.customer = Customer.objects.get(id=int(request.session['id']))
                category_obj.save()
            else:
                print("error")
        
        if request.data['type'] == "product":
            request.data.customer = request.session['id']
            form = ProductFrom(request.data)
            if form.is_valid():
                form.save()
                product_obj = form.instance
                product_obj.customer = Customer.objects.get(id=int(request.session['id']))
                product_obj.price_updated = datetime.datetime.now()
                product_obj.save()
            else:
                print("error")
        
        return Response(data={"msg": "success"}, status=status.HTTP_200_OK)
    
    if request.method == "PUT":
        print(request.data)
        if request.data['type'] == "category":
            if not Category.objects.filter(id=int(request.data['category_id'])).exists():
                return Response(data={"msg": "Category does not exists"}, status=status.HTTP_400_BAD_REQUEST)
            if not Category.objects.filter(id=int(request.data['sub_category'])).exists():
                return Response(data={"msg": "sub category does not exists"}, status=status.HTTP_400_BAD_REQUEST)
            if Category.objects.get(id=int(request.data['sub_category'])) == Category.objects.get(id=int(request.data['category_id'])):
                return Response(data={"msg": "Category and sub category cannot be same."}, status=status.HTTP_400_BAD_REQUEST)
            
            cat_obj = Category.objects.filter(id=request.data['category_id']).update(
                name=request.data['name'],
                sub_category=Category.objects.get(id=int(request.data['sub_category']))
            )
        
        if request.data['type'] == "product":
            if not Category.objects.filter(id=int(request.data['category'])).exists():
                return Response(data={"msg": "Category does not exists"}, status=status.HTTP_400_BAD_REQUEST)
            if not Product.objects.filter(id=int(request.data['product_id'])).exists():
                return Response(data={"msg": "Product does not exists"}, status=status.HTTP_400_BAD_REQUEST)
            
            product_obj = Product.objects.get(id=int(request.data['product_id']))
            if request.data['price'] != product_obj.price:
                print(product_obj.price_updated, datetime.datetime.now().date())
                if product_obj.price_updated == datetime.datetime.now().date():
                    return Response(data={"msg": "You cannot update the price twice in the same day. Please update tomorrow."}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    if datetime.datetime.now().time() > datetime.time(11, 00):
                        return Response(data={"msg": "You only update the price before 11:00 AM each day."}, status=status.HTTP_400_BAD_REQUEST)
                
                max_change = (float(product_obj.price) * 10) / 100
                current_max_price = max(float(product_obj.price), float(request.data['price']))
                current_min_price = min(float(product_obj.price), float(request.data['price']))
                if (current_max_price - current_min_price) > max_change:
                    return Response(data={"msg": "You only increase or decrease 10 percent of you current price."}, status=status.HTTP_400_BAD_REQUEST)
            
            product_obj = Product.objects.filter(id=int(request.data['product_id'])).update(
                name=request.data['name'],
                product_code=request.data['product_code'],
                price=request.data['price'],
                category=Category.objects.get(id=int(request.data['category'])),
                status=request.data['status'],
            )

        return Response(data={"msg": "success"}, status=status.HTTP_200_OK)
        # if request.POST['type'] == "delete":
        #     model = request.POST["data"].split("_")[0]
        #     del_id = request.POST["data"].split("_")[1]
        #     if model == "category":
        #         Category.objects.get(id=del_id).delete()
        #         return redirect('/products/')
        #     if model == "product":
        #         Product.objects.get(id=del_id).delete()
        #         return redirect('/products/')
        
        # if request.POST['type'] == "edit":
        #     model = request.POST["data"].split("_")[0]
        #     edit_id = request.POST["data"].split("_")[1]
        #     if model == "category":
        #         Category.objects.filter(id=edit_id).update(name=request.POST['name'])
        #         return redirect('/products/')
        #     if model == "product":
        #         product_obj = Product.objects.get(id=edit_id)
        #         product_obj.product_name = request.POST['name']
        #         product_obj.description = request.POST['description']
        #         product_obj.category = Category.objects.get(id=int(request.POST['category'][0]))
        #         product_obj.save()
        #         return redirect('/products/')

        # if request.POST['type'] == "category":
        #     form = CategoryFrom(request.data)
        #     if form.is_valid():
        #         form.save()
        #         img_obj = form.instance
        #     return redirect('/products/')
        # if request.POST['type'] == "product":
        #     form = ProductFrom(request.POST)
        #     if form.is_valid():
        #         form.save()
        #         img_obj = form.instance
            
        #     return redirect('/products/')

    if request.method == "DELETE":
        print(request.POST)
        return redirect('/products/')