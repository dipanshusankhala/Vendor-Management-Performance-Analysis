# Generated by Django 4.1.13 on 2024-05-05 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PurchaseOrder', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='issue_date',
            field=models.DateTimeField(),
        ),
    ]
