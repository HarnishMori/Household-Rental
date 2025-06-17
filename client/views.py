from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.utils.text import slugify
from django.template.response import TemplateResponse
from renters.models import Order, orderitem, Item
from . import models
from renters.views import renter_item_list
from django.urls import reverse
from . import forms
# Create your views here.
def index(request):
    products = Item.objects.all()
    profile = models.profile.objects.all()
    con = {
        "products":products,
        "profile":profile
    }
    return render(request,'index.html', context=con)

def register(request):
    if request.method == "POST":
        if request.POST.get("password1") == request.POST.get("password2"):
            try:
                User.objects.get(username = request.POST.get('username'))
                return HttpResponse("Username already exists")
            except:
                user = User.objects.create_user(username = request.POST.get('username'), password = request.POST.get('password1'))
                profile = models.profile.objects.create(user=user,
                                                        phone=request.POST.get('phone'),
                                                        email=request.POST.get('email'),
                                                        renter_or_client=request.POST.get('Role')) 
                return redirect(loginview)
        else:
            return HttpResponse("Passwords are not same")       
    return render(request, 'register.html')     


def loginview(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password1')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            try:
                profile = models.profile.objects.get(user=user)
                if profile.renter_or_client == 'C':
                    return redirect(index)
                else:
                    renter_itemlist = reverse('renters:renters_itemlist')
                    return redirect(renter_itemlist)
            except profile.DoesNotExist:
                return HttpResponse("your profile does not exist:")
        else:
            return HttpResponse("username not found")
    return render(request, 'login.html')

def itemform(request):
    user_profile = models.profile.objects.get(user=request.user)
    success_message = None
    if request.method == "POST":
        if user_profile.renter_or_client == 'R':
            title = request.POST.get('itemname')
            slug = slugify(title)
            item = Item.objects.create(
                profile=user_profile,
                title=request.POST.get('itemname'),
                slug=slug,
                price=request.POST.get('price'),
                description=request.POST.get('description'),
                image=request.FILES.get('image'),
                availability=request.POST.get('availability'))
            success_message = "Item added successfully!"
            return redirect(itemform)
        else:
            return HttpResponse("You are not registered as renter")
    return render(request, 'item_form.html',{'success_message': success_message})

def logoutview(request):
    logout(request)
    return redirect(loginview)

def checkout(request):
    if request.method ==  'POST':
        form = forms.CnfOrderForm(request.POST)
        if form.is_valid():
            cnf_order = form.save(commit=False)
            pro = models.profile.objects.get(user=request.user)
            cnf_order.profile = pro
            cnf_order.save()
            return redirect(ordercnf)
        else:
            form = forms.CnfOrderForm(request.POST)
            print(form.errors)
    return render(request, 'checkout.html', {"form":form})

def ordercnf(request):
    cnf_order = models.CnfOrder.objects.get(user=request.user)
    if cnf_order.profile.renter_or_client == 'C':
        user_profile = models.CnfOrder.objects.filter(profile__user=request.user)
        context = {"cnforder":cnf_order,"user_profile":user_profile}
        return render(request, 'ordercnf_page.html', context=context)