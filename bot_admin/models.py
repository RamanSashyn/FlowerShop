from django.db import models


class Bouquet(models.Model):
    OCCASION_CHOICES = [
        ('birthday', 'День рождения'),
        ('wedding', 'Свадьба'),
        ('school', 'В школу'),
        ('no_reason', 'Без повода'),
        ('custom', 'Другой'),
    ]

    name = models.CharField(max_length=100, verbose_name="Название букета")
    flowers = models.TextField(verbose_name="Состав букета")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена (₽)")
    image = models.ImageField(upload_to="bouquets/", blank=True, null=True, verbose_name="Фото")
    occasion = models.CharField(max_length=20, choices=OCCASION_CHOICES, blank=True, null=True, verbose_name="Повод")

    def __str__(self):
        return self.name


class Order(models.Model):
    bouquet = models.ForeignKey(Bouquet, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Букет")
    customer_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Имя клиента")
    telegram_username = models.CharField(max_length=100, blank=True, null=True, verbose_name="Telegram username")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.TextField(verbose_name="Адрес доставки")
    delivery_date = models.DateField(verbose_name="Дата доставки")
    delivery_time = models.TimeField(verbose_name="Время доставки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    status = models.CharField(max_length=50, default="в обработке", verbose_name="Статус")

    def __str__(self):
        return f"Заказ от {self.customer_name} ({self.created_at.date()})"