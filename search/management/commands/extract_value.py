from django.core.management.base import BaseCommand, CommandError
from search.utils import extract_value


class Command(BaseCommand):
    help = "Extract a hidden string value from an image using stegano."

    def add_arguments(self, parser):
        parser.add_argument("image", type=str, help="Path to the PNG image with hidden data")

    def handle(self, *args, **options):
        image = options["image"]

        try:
            value = extract_value(image)
            if value is None:
                self.stdout.write(self.style.WARNING("No hidden value found in image."))
            else:
                self.stdout.write(self.style.SUCCESS(f"Extracted value: {value}"))
        except Exception as e:
            raise CommandError(f"Error extracting value: {e}")
