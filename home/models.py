from django.db import models
from django_pandas.managers import DataFrameManager

# Create your models here.
class GeneralData(models.Model):
    year = models.CharField(max_length=250)
    casename = models.CharField(max_length=250)
    value = models.FloatField()

    objects = DataFrameManager()

class CaseData(models.Model):
    year = models.CharField(max_length=250)
    value = models.FloatField()

    objects = DataFrameManager()

class SevereData(models.Model):
    year = models.CharField(max_length=250)
    value = models.FloatField()

    objects = DataFrameManager()

class DeathData(models.Model):
    year = models.CharField(max_length=250)
    value = models.FloatField()

    objects = DataFrameManager()

