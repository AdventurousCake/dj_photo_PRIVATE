from django.db import models
from django.utils.translation import gettext as _


class MenuItem(models.Model):
    id = models.BigAutoField(null=False, unique=True, primary_key=True,
                             auto_created=True)
    json = models.JSONField(null=False, max_length=150, blank=False)

    created_date = models.DateTimeField(null=False, auto_now_add=True)
    updated_date = models.DateTimeField(null=False, auto_now=True)


class PhotoItem(models.Model):
    id = models.BigAutoField(null=False, unique=True, primary_key=True,
                             auto_created=True)
    author = models.CharField(null=False, max_length=150)  # o2m
    description = models.CharField(null=True, max_length=150)
    # names = models.CharField(null=True, max_length=150)  # list in pgsql
    # https://docs.djangoproject.com/en/4.1/ref/contrib/postgres/fields/#django.contrib.postgres.fields.ArrayField

    names = models.JSONField(null=True, max_length=150, default=[])
    created_date = models.DateTimeField(null=False, auto_now_add=True)

    lat = models.DecimalField(_('Latitude'), max_digits=10, decimal_places=8)
    long = models.DecimalField(_('Longitude'), max_digits=11, decimal_places=8)