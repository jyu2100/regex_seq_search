from django.core.management.base import BaseCommand
from search.utils import run_search

class Command(BaseCommand):
    help = "Nucleotide sequence search from the command line"

    def add_arguments(self, parser):
        parser.add_argument("pattern", type=str, help="Regex pattern")
        parser.add_argument("uid", type=str, help="UID")

    def handle(self, *args, **options):
        try:
            pattern = options["pattern"]
            uid = options["uid"]

            matches = run_search(pattern, uid)

            for sequence in matches:
                self.stdout.write(self.style.SUCCESS(f'{sequence}'))

                for start, end in matches[sequence]:
                    self.stdout.write(self.style.SUCCESS(f'  {start}-{end}'))

                self.stdout.write(self.style.SUCCESS(''))

        except Exception as e:
            self.stdout.write(self.style.ERROR(e))


