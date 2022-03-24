# Generated by Django 4.0.3 on 2022-03-24 09:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('promoapp', '0004_coupon_discounttype_coupon_max_coupen_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_coupen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_coupen', to='promoapp.coupon'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_user', to=settings.AUTH_USER_MODEL),
        ),
    ]