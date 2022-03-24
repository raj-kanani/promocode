from django import forms
from .models import Coupon



class AddCouponForm(forms.ModelForm):
    code = forms.CharField(max_length=4000)
    class Meta:
        model = Coupon
        fields = '__all__'






