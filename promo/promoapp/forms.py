from django import forms
from .models import Coupon


class AddCouponForm(forms.ModelForm):
    code = forms.CharField(max_length=40)

    class Meta:
        model = Coupon
        fields = '__all__'
