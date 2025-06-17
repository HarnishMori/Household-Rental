from django.contrib import admin
from renters.models import Item, orderitem, Order
# Register your models here.


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('title',)}

admin.site.register(Order)
admin.site.register(orderitem)