# blog/management/commands/warm_blog_cache.py
from django.core.management.base import BaseCommand
from blog.blog_caching import warm_all_blog_cache


class Command(BaseCommand):
    help = "Pre-caches all BlogPost list pages and individual post details in Redis"

    def handle(self, *args, **options):
        self.stdout.write("Warming BlogPost list and detail caches...")
        warm_all_blog_cache()
        self.stdout.write(self.style.SUCCESS("Blog cache successfully warmed!"))