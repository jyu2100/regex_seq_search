from django.core.management.base import BaseCommand, CommandError
from search.utils import embed_value


class Command(BaseCommand):
    help = "Embed a string value into an image using stegano."

    def add_arguments(self, parser):
        parser.add_argument("input_image", type=str, help="Path to the input PNG image")
        parser.add_argument("output_image", type=str, help="Path to save the PNG with hidden data")
        parser.add_argument("value", type=str, help="The string value to embed")

    def handle(self, *args, **options):
        input_image = options["input_image"]
        output_image = options["output_image"]
        value = options["value"]

        try:
            embed_value(input_image, output_image, value)
            self.stdout.write(self.style.SUCCESS(
                f"Successfully embedded value into {output_image}"
            ))
        except Exception as e:
            raise CommandError(f"Error embedding value: {e}")
