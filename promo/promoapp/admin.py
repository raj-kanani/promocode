from django.contrib import admin
from .models import Coupon, UserData


# @admin.register(Coupon)
# class CoupenAdmin(admin.ModelAdmin):
#     list_display = ['id', 'code', 'gender', 'start_date', 'end_date', 'discount']
#     list_filter = ['start_date', 'end_date']
#     search_fields = ['id']
#


admin.site.register(UserData)
admin.site.register(Coupon)