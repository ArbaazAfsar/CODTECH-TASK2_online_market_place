# Generated by Django 5.1.1 on 2024-12-29 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_order_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='seller_approval',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Cancelled', 'Cancelled'), ('Completed', 'Completed')], default='Pending', max_length=20),
        ),
    ]
