from django.db import models
from store.models import Item

class LaptopSpecs(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE, related_name="laptopspecs")

    ram = models.PositiveIntegerField(null=True, blank=True)
    storage = models.PositiveIntegerField(null=True, blank=True)
    processor = models.CharField(max_length=100, null=True, blank=True)
    operating_system = models.CharField(max_length=100, null=True, blank=True)
    screen_size = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    battery_life = models.CharField(max_length=50, null=True, blank=True)
    resolution = models.CharField(max_length=50, null=True, blank=True)
    hdmi_support = models.BooleanField(default=False)
    bluetooth = models.BooleanField(default=False)
    wifi = models.BooleanField(default=False)
    battery_life = models.CharField(max_length=50, blank=True, null=True) 