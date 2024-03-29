# Generated by Django 2.0.7 on 2018-07-22 22:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('phone_number', models.CharField(max_length=10, unique=True)),
                ('country_code', models.CharField(default='1', max_length=3)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone_number_verified', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ethereum_address', models.CharField(max_length=42, verbose_name='Ethereum address')),
                ('count', models.PositiveIntegerField(default=0)),
                ('on_receive', models.BooleanField()),
                ('on_send', models.BooleanField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('txHash', models.CharField(max_length=66)),
                ('block', models.IntegerField()),
                ('_from', models.CharField(max_length=42)),
                ('to', models.CharField(max_length=42)),
                ('eth_value', models.DecimalField(decimal_places=18, max_digits=30)),
                ('link', models.URLField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('task_id', models.CharField(blank=True, editable=False, max_length=50)),
                ('alert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Alert')),
            ],
        ),
    ]
