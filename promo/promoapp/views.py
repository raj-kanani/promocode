from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import RedirectView

from .models import Coupon
from .forms import AddCouponForm


def addCoupon(request):
    if request.method == 'POST':
        form = AddCouponForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Your coupon has been saved successfully!')
    else:
        form = AddCouponForm()
    return render(request, 'coupen-add.html', {'form': form})


def showcoupen(request):
    sc = Coupon.objects.all()
    return render(request, 'coupen-show.html', {'coupen': sc})


class updatecoupen(View):
    def get(self, request, id):
        s = Coupon.objects.get(id=id)
        print(s.id)
        fm = AddCouponForm(instance=s)
        return render(request, 'coupen-edit.html', {'sc': fm})

    def post(self, request, id):
        s = Coupon.objects.get(id=id)
        fm = AddCouponForm(request.POST, instance=s)
        if fm.is_valid():
            fm.save()
            return HttpResponseRedirect('/show/')


# def updatecoupen(request, id):
#     cp = Coupon.objects.get(pk=id)
#     count_coupen = cp.coupon_related.filter().count()
#     if request.method == "POST":
#         form = AddCouponForm(request.POST, instance=cp)
#         cd = request.POST.get('code')
#
#         if form.is_valid():
#             if count_coupen:
#                 messages.info("Dont change coupen")
#             else:
#                 cp = cd
#                 form.save()
#                 return redirect('/show/')
#         else:
#             messages.error("invalid")
#     else:
#         form = AddCouponForm(instance=cp)
#         return render(request, 'coupen-edit.html', {'coupen': cp, 'form': form})


def deletecoupen(request):
    dc = Coupon.objects.get(id=id)
    dc.delete()
    return redirect('/show/')

#
# def deletecoupen(request, id):
#     coupon = Coupon.objects.get(id=id)
#     count_order = Coupon.objects.filter().count()
#
#     if count_order:
#         return HttpResponse("You can not delete coupon")
#     else:
#         coupon.delete()
#         return redirect('/show/')
#

# class Deletecoupen(RedirectView):
#     url = '/show/'
#
#     def get_redirect_url(self, *args, **kwargs):
#         print('delete-data', kwargs)
#         d = kwargs['id']
#         Coupon.objects.get(id=d).delete()
#         ''' obj = Todos.objects.get(id=kwargs['id'])'''
#         '''obj.delete()'''
#         return super().get_redirect_url(*args, **kwargs)
