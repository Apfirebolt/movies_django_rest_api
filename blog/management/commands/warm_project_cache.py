from django.core.management.base import BaseCommand
from blog.caching import warm_projects_cache


class Command(BaseCommand):
    help = "Pre-caches all paginated pages of projects in Redis"

    def handle(self, *args, **options):
        self.stdout.write("Warming Projects cache...")
        warm_projects_cache()
        self.stdout.write(self.style.SUCCESS("Projects cache successfully warmed!"))