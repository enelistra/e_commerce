from django import views
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages,auth
from.models import cart, newupdates
from django.db.models import Q
from django.contrib.auth import logout

# Create your views here.

def register(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('pass')
        cpass=request.POST.get('cfmpass')
        if password==cpass:
            if User.objects.filter(username=username).exists():
                messages.info(request,'username already exists')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'email already exists')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()
                return render(request,'login.html')
        else:
            messages.info(request,'password not matching')
            return render(request,'register.html')
    return render(request,'register.html')

def login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=auth.authenticate(username=username,password=password)
        if User is not None:
            auth.login(request,user)
            return redirect('index')
        else:
            messages.error(request,'invalid username or password')
            return render (request,'login.html')
    return render(request,'login.html')

def index(request):
    obj = newupdates.objects.all()
    user=request.user
    number = cart.objects.filter(user=user)
    items_taken = number.count()
    name = user.username
    return render(request,'index.html',{'obj':obj,'items_taken':items_taken,'name':name})

def details(request,product_id):
    product=newupdates.objects.get(id=product_id)
    user=request.user
    name = user.username
    number = cart.objects.filter(user=user)
    items_taken = number.count()
    return render(request,'details.html',{'product':product,'name':name,'items_taken':items_taken})

def mycart(request,product_id):
    user=request.user
    obj=cart.objects.filter(user=user)
    if request.method=='POST':
        product=newupdates.objects.get(id=product_id)
        mycart=cart(product = product , user = user)
        mycart.save()
        obj=cart.objects.filter(user=user)
    items_taken = obj.count()
    cost = 0
    for item in obj:
        cost += item.product.price
    user=request.user
    number = cart.objects.filter(user=user)
    items_taken = number.count()
    name = user.username
    return render(request,'mycart.html',{'obj':obj,'cost':cost,'items_taken':items_taken,'name':name})

def delete(request,cart_id):
    cart_items=cart.objects.get(id=cart_id)
    cart_items.delete()
    user=request.user
    obj=cart.objects.filter(user=user)
    items_taken = obj.count()
    cost = 0
    for item in obj:
        cost += item.product.price
    return render(request,'mycart.html',{'obj':obj,'items_taken':items_taken,'cost':cost})

def search(request):
    user = request.user
    obj=cart.objects.filter(user=user)
    items_taken = obj.count()
    if 'q' in request.GET:
        query_string = request.GET.get('q')
        search_results = newupdates.objects.filter(Q(brand__icontains=query_string)| Q(category__icontains=query_string) | Q(desc__icontains=query_string))
        return render(request, 'search_result.html', {'search_results': search_results,'items_taken':items_taken})
    else:
        return render(request, 'search_result.html', {'search_results': None,'items_taken':items_taken})


def user_logout(request):
    logout(request)
    return redirect('login')
