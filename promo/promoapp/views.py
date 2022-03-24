import datetime
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

from django.views import View
from django.views.generic import RedirectView

from .models import Coupon, UserData, Order
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


# def addorder(request):
#     form = AddCouponForm(request.post)
#     if form.is_valid():
#         code = form.cleaned_data.get('code')
#         order = Order.objects.get(user=request.user, complete=False)
#         # ud = UserData.objects.filter(birth_date='birth_date')
#         coupon = Coupon.objects.filter(code=code)
#         if not coupon:
#             messages.error('coupon does not exist')
#             return redirect('/addorder/')
#         else:
#             try:
#                 coupon.used += 3
#                 coupon.save()
#                 order.coupon = coupon
#                 order.save()
#                 messages.success("Successfully added coupon")
#             except:
#                 messages.error("you dont use  coupon")
#
#             return redirect('/show/')


def addorder(request):
    if request.method == "POST":
        order_coupen = request.POST.get('order_coupen')
        order_amount = int(request.POST.get('order_amount'))

        c = Coupon.objects.filter(code=request.POST.get('order_coupen')).first()

        user = UserData.objects.filter(birth_date=request.user.birth_date).first()
        # if not c:
        #     return HttpResponse('doesnot exist')

        if c.discounttype == 'Flat':
            order_total = order_amount - c.discount
        else:
            birthdate = user.birth_date
            today_date = datetime.date.today()
            valid = timezone.now().date().strftime("%m-%d")
            if birthdate and birthdate.strftime("%m-%d") == valid:
                discount = order_amount * (c.discount / 100)

                total = order_amount - discount
                order_total = total - (total * 0.1)
            else:
                discount = order_amount * (c.discount / 100)
                order_total = order_amount - discount
        try:
            limit = c.user_limit
            max = c.max_coupen

            if user.is_authenticated:
                uc = user.order_user.count()
                cc = c.my_coupen.count()

                if cc < max:
                    if uc >= limit:
                        return HttpResponse("Per user limit is over")
                    new = Order.objects.create(order_coupen=c, order_amount=order_amount, order_total=order_total,
                                               user=request.user)
                    new.save()
                else:
                    return HttpResponse("sorry limited coupen")
        except:
            create_order = Order.objects.create(order_coupen=c, order_amount=order_amount,
                                                order_total=order_total, user=request.user)
            create_order.used += 1
            create_order.save()
        return redirect('/showorder/')
    else:
        return render(request, 'order-add.html')


def showorder(request):
    so = Order.objects.all()
    return render(request, 'order-show.html', {'so': so})


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


# def deletecoupen(request):
#     dc = Coupon.objects.get(id=id)
#     dc.delete()
#     return redirect('/show/')

class Deletecoupen(RedirectView):
    url = '/show/'

    def get_redirect_url(self, *args, **kwargs):
        print('delete-data', kwargs)
        # d = kwargs['id']
        # Coupon.objects.get(id=d).delete()
        obj = Coupon.objects.get(id=kwargs['id'])
        obj.delete()
        return super().get_redirect_url(*args, **kwargs)
