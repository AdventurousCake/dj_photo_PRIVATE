from django.db import models
from django.db.models import Sum
from django.utils.text import gettext_lazy as _


class Curr(models.TextChoices):
    EUR = 'EUR', _('Euro')
    GBP = 'GBP', _('British Pound')
    USD = 'USD', _('US Dollar')
    RUB = 'RUB', _('Russian Ruble')


class Item(models.Model):
    class Curr(models.TextChoices):
        EUR = 'EUR', 'Euro'
        GBP = 'GBP', 'British Pound'
        USD = 'USD', 'US Dollar'
        RUB = 'RUB', 'Russian Ruble'

    id = models.BigAutoField(primary_key=True, auto_created=True, null=False)
    price = models.DecimalField(max_digits=9, decimal_places=2, null=False)
    description = models.CharField(max_length=256, null=True, blank=True)

    currency = models.CharField(choices=Curr.choices, null=False, blank=True, default=Curr.RUB, max_length=50)

    def __str__(self):
        return f"{self.id}: {self.price}"


class Order(models.Model):
    id = models.BigAutoField(primary_key=True, auto_created=True, null=False)
    items = models.ManyToManyField(to=Item)  # symmetrical?

    def get_total_cost(self):
        return self.items.aggregate(Sum('price')).get('price__sum')

    def get_discount_total_cost(self):
        # x / 100 * (100-discount)
        pass
        # return self.get_total_cost()/100 * (self.discount.first())

    def get_disc(self):
        # return self.discount_set.all()
        return self.discount_set.first().value

    def __str__(self):
        return f"total {self.get_total_cost()}; disc: {self.get_disc()}"


# from stripe_service.models import Order2, Item
#  Order2.objects.get(pk=1).discount2_set.first().value
# todo https://metanit.com/python/django/5.7.php

class Discount(models.Model):
    id = models.BigAutoField(primary_key=True, auto_created=True, null=False)
    orders = models.ManyToManyField(to=Order, related_name='discount_set')  # related_name='discount')  # symmetrical?
    value = models.IntegerField(null=False, default=5)
    valid_until_date = models.DateTimeField()

    class Meta:
        pass
        # unique?


class Order2(models.Model):
    items = models.ManyToManyField(Item)

    def __str__(self):
        return f"total: {self.total_cost}; disc: {self.disc}"

    @property
    def total_cost(self):
        return self.items.aggregate(Sum('price'))['price__sum']

    @property
    def disc(self):
        return self.discount2_set.all()

    # @property
    # def discount_total_cost(self):
    #     pass
    #     # return self.total_cost / 100 * (100 - self.discount.value)


class Discount2(models.Model):
    orders = models.ManyToManyField(Order2, related_name='discount2_set')
    value = models.PositiveIntegerField(default=5)
    valid_until_date = models.DateTimeField()
