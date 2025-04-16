from django.db import models
from store.models import Item

class TabletSpecs(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE, related_name='tabletspecs')
    screen_size = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    resolution = models.CharField(max_length=50, blank=True, null=True)
    ram = models.PositiveIntegerField(blank=True, null=True)
    storage = models.PositiveIntegerField(blank=True, null=True)
    battery_capacity = models.PositiveIntegerField(blank=True, null=True)
    operating_system = models.CharField(max_length=100, blank=True, null=True)
    sim_support = models.BooleanField(default=False)
    touchscreen = models.BooleanField(default=True)
    bluetooth = models.BooleanField(default=False)
    wifi = models.BooleanField(default=False)

    def __str__(self):
        return f"Tablet Specs for {self.item.name}"
