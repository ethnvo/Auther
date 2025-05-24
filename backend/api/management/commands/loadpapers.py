from django.core.management.base import BaseCommand
from api.scripts.load_papers import run

class Command(BaseCommand):
    help = 'Fetch and save academic papers with gender tagging'

    def handle(self, *args, **kwargs):
        run()
