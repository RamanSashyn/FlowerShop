# Generated by Django 5.1.4 on 2025-03-26 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsultationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100, verbose_name='Имя клиента')),
                ('telegram_username', models.CharField(blank=True, max_length=100, null=True, verbose_name='Username Telegram')),
                ('phone_number', models.CharField(max_length=30, verbose_name='Номер телефона')),
                ('submitted_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время запроса')),
            ],
        ),
    ]
