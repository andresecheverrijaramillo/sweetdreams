# Generated by Django 4.2.4 on 2023-11-06 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_rename_orders_order_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductJson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('productJson_id', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product_image', models.URLField()),
            ],
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
