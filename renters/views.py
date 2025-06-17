from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils import timezone
from django.utils.text import slugify
from .models import Item, orderitem, Order
from client.models import profile
from django.urls import reverse

# Create your views here.

class checkoutview(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            con = {'order':order}
            return render(self.request, 'checkout.html', context=con)
        except ObjectDoesNotExist as e:
            print('error', e)
            con = {'messege':'No object found'}
            return render(self.request,'checkout.html', context=con)

class ItemList(ListView):
    model = Item
    template_name = 'category.html'
    context_object_name = 'items'
    paginate_by = 2

class ItemDetail(DetailView):
    model = Item
    template_name = 'single-product.html'
    context_object_name = 'items'

class Cartview(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            # print('User:', self.request.user)
            order = Order.objects.get(user=self.request.user, ordered=False)
            # print('order:', order)
            context = {'order':order}
            return render(self.request, 'cart.html', context=context)
        except ObjectDoesNotExist as e:
            print('error:', e)
            context = {'message':'No active Order Found'}
            return render(self.request, 'cart.html', context=context)

@login_required
def renter_item_list(request):
    user_profile = Item.objects.filter(profile__user=request.user)
    user = profile.objects.get(user=request.user)
    context = {"user_profile":user_profile}
    return render(request, 'renter_itemlist.html', context=context)

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = orderitem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request, "This Item is updated")
            return redirect("renters:cart")
        else:
            order.items.add(order_item)
            messages.success(request, "This item was added to your Cart")
            return redirect("renters:cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.success(request, "This item was added to your Cart")
        return redirect("renters:cart")

@login_required
def add_single_itme_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = orderitem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request, "This item was updated")
            return redirect("renters:cart")
        
@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #check order is exists 
        if order.items.filter(item__slug=item.slug).exists():
            order_item, created = orderitem.objects.get_or_create(
                item=item,
                user=request.user,
                ordered=False
            )
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, "item quantity is updated")
            else:
                order.items.remove(order_item)
                messages.info(request, "Item was removed")
            return redirect("renters:cart")            
        
def deleteview(request, pk):
    dlt_data = Item.objects.get(pk=pk)
    dlt_data.delete()
    user_profile = Item.objects.filter(profile__user=request.user)
    user = profile.objects.get(user=request.user)
    context = {"user_profile":user_profile}
    return render(request, 'renter_itemlist.html', context=context)

def edit(request, pk):
    item = Item.objects.get(pk=pk)
    print(item)
    # user_profile = Item.objects.filter(profile__user=request.user)
    # user = profile.objects.get(user=request.user)
    context = {"item":item}
    return render(request, 'edit_item_form.html', context=context)

def update(request, pk):
    user_profile = Item.objects.filter(profile__user=request.user)
    user = profile.objects.get(user=request.user)
    item = Item.objects.get(pk=pk)
    success_message = None

    # Check if the user is authorized to update the item
    # if item.profile.user != request.user:
    #     return HttpResponse("You are not authorized to update this item")

    if request.method == "POST":
        if user.renter_or_client == 'R':
            title = request.POST.get('itemname')
            slug = slugify(title)
            item.title = title
            item.slug = slug
            item.price = request.POST.get('price')
            item.description = request.POST.get('description')
            if request.FILES.get('image'):
                item.image = request.FILES.get('image')
            item.availability = request.POST.get('availability')
            item.save()
            success_message = "Item updated successfully!"
        else:
            return HttpResponse("You are not registered as a renter")
    renter_itemlist = reverse('renters:renters_itemlist')
    return redirect(renter_itemlist, {'item': item, 'success_message': success_message})

