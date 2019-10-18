# Generated by Django 2.2.4 on 2019-10-18 03:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AlterField(
            model_name='product',
            name='user',
            field=models.ManyToManyField(related_name='product_id', to=settings.AUTH_USER_MODEL),
        ),
    ]
