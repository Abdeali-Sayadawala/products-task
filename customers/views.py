from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Customer

# Create your views here.
def register(request):
    if request.method == "GET":
        error=False
        return render(request, "register.html", context={"error": error})
    
    if request.method == "POST":
        error = False
        if Customer.objects.filter(email=request.POST['email']).exists():
            return render(request, "register.html", context={"error": "Email already exists!"})
        customer_obj = Customer.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            password=make_password(request.POST['password'], salt="salt")
        )
        customer_obj.save()
        request.session['id'] = str(customer_obj.id)
        request.session['name'] = request.POST['name']
        request.session['email'] = request.POST['email']
        # return render(request, "register.html", context={"error": error})
        return redirect('/products/')


def login(request):
    if request.method == "GET":
        error=False
        return render(request, "login.html", context={"error": error})
    
    if request.method == "POST":
        print(request.POST)
        if not Customer.objects.filter(email=request.POST['email']).exists():
            return render(request, "login.html", context={"error": "Email does not exists!"})
        
        user_obj = Customer.objects.get(email=request.POST['email'])
        if check_password(request.POST["password"], user_obj.password):
            request.session['id'] = str(user_obj.id)
            request.session['name'] = user_obj.name
            request.session['email'] = user_obj.email
        else:
            return render(request, "login.html", context={"error": "Incorrect password!"})
        # return render(request, "login.html", context={"error": "Login successfull"})
        return redirect('/products/')

def logout(request):
    del request.session['id']
    del request.session['name']
    del request.session['email']
    # return render(request, "login.html", context={"error": error})
    return redirect('/login/')

def to_login(request):
    return redirect('/login/')