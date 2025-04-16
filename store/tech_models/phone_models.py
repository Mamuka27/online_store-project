
from django.db import models
from store.models import Item

class PhoneSpecs(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE, related_name='phonespecs')
    screen_size = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    resolution = models.CharField(max_length=50, null=True, blank=True)
    ram = models.PositiveIntegerField(null=True, blank=True)
    storage = models.PositiveIntegerField(null=True, blank=True)
    operating_system = models.CharField(max_length=100, null=True, blank=True)
    battery_capacity = models.PositiveIntegerField(null=True, blank=True)
    fast_charging = models.BooleanField(default=False)
    sim_support = models.BooleanField(default=False)
    touchscreen = models.BooleanField(default=False)
    bluetooth = models.BooleanField(default=False)
    wifi = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.item.name} Specs"
