# Generated by Django 5.0.7 on 2024-07-15 23:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_hotel_hotel_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('contact_info', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='RestaurantOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('delivery_date', models.DateTimeField()),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed')], max_length=20)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.provider')),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.reservation')),
            ],
        ),
        migrations.CreateModel(
            name='AdditionalService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('requested', 'Requested'), ('confirmed', 'Confirmed'), ('completed', 'Completed')], default='requested', max_length=10)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.reservation')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.service')),
            ],
        ),
    ]