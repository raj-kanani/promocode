# Generated by Django 4.0.3 on 2022-03-24 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promoapp', '0009_alter_coupon_discounttype_alter_order_order_coupen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='discounttype',
            field=models.CharField(choices=[('Flat', 'flat'), ('Discount', 'discount')], default='Flat', max_length=10),
        ),
    ]