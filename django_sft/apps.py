# -*- coding: utf-8
from django.apps import AppConfig
from django.conf import settings
from django.utils.autoreload import autoreload_started

from django_sft.compiler import sft_compile


def watch_sft(sender, **kwargs):
    sender.watch_dir('tests/example', '**/*.sft')

class DjangoSftConfig(AppConfig):
    name = 'django_sft'

    def ready(self):
        if settings.DEBUG:
            sft_compile()
            autoreload_started.connect(watch_sft)
