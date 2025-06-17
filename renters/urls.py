from django.urls import path,include
from renters import views
from django.views.generic import TemplateView

app_name = 'renters'

urlpatterns = [
    path('abc/',views.ItemList.as_view(), name='item_view'),
    path('cart/', views.Cartview.as_view(), name='cart'),
    path('checkout/', views.checkoutview.as_view(), name='checkout'),
    path('item_detail/<slug:slug>/', views.ItemDetail.as_view(), name='item_details'),
    path('add/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('add_single_item_to_cart/<slug:slug>/', views.add_single_itme_to_cart, name='add_single_item_to_cart'),
    path('remove_single_item_from_cart/<slug:slug>/', views.remove_single_item_from_cart, name='remove_single_item_from_cart'),
    path('renters_itemlist/', views.renter_item_list, name='renters_itemlist'),
    path('delete/<int:pk>/', views.deleteview, name='deleteview'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('update/<int:pk>/', views.update, name='update'),
]