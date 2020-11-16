from django.core.management.base import BaseCommand, CommandError

from django_sft.compiler import sft_compile


class Command(BaseCommand):
    help = 'Compile all SFT files'

    def handle(self, *args, **options):
        try:
            self.stdout.write('Starting to compile SFTs')
            sft_compile()
            self.stdout.write(self.style.SUCCESS('Success!'))
        except Exception as e:
            raise CommandError('Something went wrong with compiling: {}'.format(e))
