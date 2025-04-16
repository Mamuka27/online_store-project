from django.core.management.base import BaseCommand
from store.models import Item
from store.tech_models.tv_models import TVSpecs

class Command(BaseCommand):
    help = "Migrate TV specs from existing Item data to TVSpecs"

    def handle(self, *args, **kwargs):
        items = Item.objects.filter(subcategory__name__iexact="tv")

        for item in items:
            if not hasattr(item, "tvspecs"):
                TVSpecs.objects.create(
                    item=item,
                    screen_size=None,
                    resolution=None,
                    smart_tv=False,
                    operating_system=None,
                    hdmi_ports=None,
                    usb_ports=None,
                    bluetooth=False,
                    wifi=False,
                    hdr_support=False,
                    refresh_rate=None
                )
                self.stdout.write(self.style.SUCCESS(f"✅ Migrated (default): {item.name}"))
            else:
                self.stdout.write(self.style.NOTICE(f"⚠️ Already has specs: {item.name}"))
