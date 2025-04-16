from django.core.management.base import BaseCommand
from store.models import Item
from store.tech_models.tablet_models import TabletSpecs

class Command(BaseCommand):
    help = "Migrate tablet data to TabletSpecs model"

    def handle(self, *args, **kwargs):
        tablets = Item.objects.filter(subcategory__name__iexact='tablets')
        for item in tablets:
            if not hasattr(item, 'tabletspecs'):
                TabletSpecs.objects.create(
                    item=item,
                    screen_size=getattr(item, 'screen_size', None),
                    resolution=getattr(item, 'resolution', None),
                    ram=getattr(item, 'ram', None),
                    storage=getattr(item, 'storage', None),
                    battery_capacity=getattr(item, 'battery_capacity', None),
                    operating_system=getattr(item, 'operating_system', None),
                    sim_support=getattr(item, 'sim_support', False),
                    touchscreen=getattr(item, 'touchscreen', False),
                    bluetooth=getattr(item, 'bluetooth', False),
                    wifi=getattr(item, 'wifi', False),
                )
                self.stdout.write(self.style.SUCCESS(f"✅ Migrated: {item.name}"))
