from django.urls import path
from .import views

urlpatterns = [

        path('add/', views.addCoupon, name='add'),
        path('show/', views.showcoupen, name='show'),
        path('addorder/', views.addorder, name='addorder'),
        path('showorder/', views.showorder, name='showorder'),
        path('update/<int:id>/', views.updatecoupen.as_view(), name='update'),
        path('delete/<int:id>/', views.Deletecoupen.as_view(), name='delete'),

]
