import datetime
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
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
        # order_coupen = request.POST['order_coupen']
        order_coupen = request.POST.get('order_coupen')
        order_amount = int(request.POST.get('order_amount'))

        c = Coupon.objects.filter(code=request.POST.get('order_coupen')).first()

        user = UserData.objects.filter(birth_date=request.user.birth_date).first()

        if c.discounttype == 'flat':
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

            max_limit = c.max_coupen
            user_limit = c.user_limit

            if user.is_authenticated:
                user_count = len(Order.objects.filter(user=user, order_coupen=c))
                coupon_count = len(Order.objects.filter(order_coupen=c))

                if coupon_count > user_limit:
                    return HttpResponse(" coupon limit over ")

                if user_count > max_limit:
                    return HttpResponse("Per user limit is over")

                new_order = Order.objects.create(order_coupen=c, order_amount=order_amount, order_total=order_total,
                                                 user=request.user)

                c.max_coupen = c.max_coupen - 1
                c.save()
                return redirect('showorder')
            else:

                return HttpResponse("Coupon limit is over")
        except Exception as e:
            return HttpResponse(e.__str__())


    else:
        return render(request, 'order-add.html')


def showorder(request):
    so = Order.objects.all()
    return render(request, 'order-show.html', {'so': so})


def updatecoupon(request, id):
    cp = Coupon.objects.get(pk=id)
    order_count = cp.my_coupen.filter().count()

    if request.method == "POST":
        form = AddCouponForm(request.POST, instance=cp)
        c = request.POST.get('code')

        if form.is_valid():
            if order_count:
                return HttpResponse("you can not change used coupon")
            else:
                cp = c
                form.save()
                return redirect('show')
        else:
            print(form.errors)
    else:
        form = AddCouponForm(instance=cp)
        return render(request, 'coupen-edit.html', {'coupon': cp, 'form': form})


# class updatecoupen(View):
#     def get(self, request, id):
#         s = Coupon.objects.get(id=id)
#         # print(s.id)
#         fm = AddCouponForm(instance=s)
#         return render(request, 'coupen-edit.html', {'sc': fm})
#
#     def post(self, request, id):
#         s = Coupon.objects.get(id=id)
#         fm = AddCouponForm(request.POST, instance=s)
#         if fm.is_valid():
#             fm.save()
#             return HttpResponseRedirect('/show/')

def deletecoupon(request, id):
    coupon = Coupon.objects.get(pk=id)
    data_count = coupon.my_coupen.filter().count()

    if data_count:
        return HttpResponse("Used coupon don't delete")
    else:
        coupon.delete()
        return redirect('show')

#
# try:
#            limit = c.user_limit
#            max = c.max_coupen
#
#            if user.is_authenticated:
#                uc = user.order_user.count()
#                cc = c.my_coupen.count()
#
#                if cc > max:
#                    if uc >= limit:
#                        return HttpResponse(" only 3 coupon used per user ")
#
#                    new_order = Order.objects.create(order_coupen=c, order_amount=order_amount, order_total=order_total,
#                                                     user=request.user)
#                    new_order.save()
#                else:
#                    return HttpResponse(" don't access same coupon multiple time..")
#        except:
#            new_order = Order.objects.create(order_coupen=c, order_amount=order_amount,
#                                             order_total=order_total, user=request.user)
#
#            new_order.used += 1
#            new_order.save()
#        return redirect('/showorder/')
