from django.db import models
from store.models import Item

class TVSpecs(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE, related_name="tvspecs")
    screen_size = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True, help_text="In inches")
    resolution = models.CharField(max_length=50, blank=True, null=True)
    smart_tv = models.BooleanField(default=False)
    operating_system = models.CharField(max_length=100, blank=True, null=True)
    hdmi_ports = models.PositiveIntegerField(blank=True, null=True)
    usb_ports = models.PositiveIntegerField(blank=True, null=True)
    bluetooth = models.BooleanField(default=False)
    wifi = models.BooleanField(default=False)
    hdr_support = models.BooleanField(default=False)
    refresh_rate = models.PositiveIntegerField(blank=True, null=True, help_text="In Hz")

    def __str__(self):
        return f"{self.item.name} TV Specs"
