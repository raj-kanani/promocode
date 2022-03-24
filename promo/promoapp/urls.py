from django.urls import path
from .import views

urlpatterns = [

        path('add/', views.addCoupon, name='add'),
        path('show/', views.showcoupen, name='show'),
        path('update/<int:id>/', views.updatecoupen.as_view(), name='update'),
        path('delete/<int:id>/', views.deletecoupen, name='delete'),

]
