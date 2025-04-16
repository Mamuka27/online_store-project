from django.core.management.base import BaseCommand
from store.models import Item
from store.tech_models.laptop_models import LaptopSpecs

class Command(BaseCommand):
    help = "Migrate existing laptop item fields into LaptopSpecs"

    def handle(self, *args, **kwargs):
        laptops = Item.objects.filter(subcategory__name__iexact='laptops')
        for item in laptops:
            if not hasattr(item, 'laptopspecs'):
                LaptopSpecs.objects.create(
                    item=item,
                    ram=item.ram,
                    storage=item.storage,
                    screen_size=item.screen_size,
                    resolution=item.resolution,
                    operating_system=item.operating_system,
                    bluetooth=item.bluetooth,
                    wifi=item.wifi,
                    hdmi_support=item.hdmi_support
                )
                self.stdout.write(self.style.SUCCESS(f"Migrated: {item.name}"))
