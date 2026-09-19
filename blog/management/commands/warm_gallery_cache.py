# blog/management/commands/warm_gallery_cache.py
from django.core.management.base import BaseCommand
from blog.gallery_caching import warm_all_gallery_cache


class Command(BaseCommand):
    help = "Pre-caches all gallery list pages and individual post details in Redis"

    def handle(self, *args, **options):
        self.stdout.write("Warming Gallery list and detail caches...")
        warm_all_gallery_cache()
        self.stdout.write(self.style.SUCCESS("Gallery cache successfully warmed!"))