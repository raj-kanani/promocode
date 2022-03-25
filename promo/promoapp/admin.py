from django.contrib import admin
from .models import Coupon, UserData, Order

admin.site.register(UserData)


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'gender', 'start_date', 'end_date', 'discount']
    list_filter = ['start_date', 'end_date']
    search_fields = ['id']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'used', 'order_amount', 'order_total', 'order_coupen']

# @admin.register(Order)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('order_coupen', 'order_amount')
#     actions = ['discount_30']
#
#     def discount_30(self, request, queryset):
#         discount = 30  # percentage
#
#         for product in queryset:
#             """ Set a discount of 30% to selected products """
#             multiplier = discount / 100.  # discount / 100 in python 3
#             old_price = Order.order_total
#
#             Order.price = old_price
#             Order.save()
#
#     discount_30.short_description = 'Set 30%% discount'
