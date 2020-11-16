from html.parser import HTMLParser
from pathlib import Path
import re


EXTENDS_REGEX_PATTERN = '\{\% extends [\'"](?P<template>.*?)[\'"]'
extends_regex = re.compile(EXTENDS_REGEX_PATTERN)


class TemplateParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.html_start = None
        self.html_end = None
        self.script_start = None
        self.script_end = None
        self.style_start = None
        self.style_end = None
        self.head_end = None
        self.body_end = None

    def handle_starttag(self, tag, attrs):
        if tag == 'template' and self.html_start is None:
            self.html_start = self.getpos()[0]
            return
        if tag == 'script' and self.script_start is None and self.html_end is not None:
            self.script_start = self.getpos()[0]
            return
        if tag == 'style' and self.style_start is None and self.html_end is not None:
            self.style_start = self.getpos()[0]
            return

    def handle_endtag(self, tag):
        if tag == 'template' and self.html_end is None:
            self.html_end = self.getpos()[0]
            return
        if tag == 'script' and self.script_end is None and self.script_start is not None:
            self.script_end = self.getpos()[0]
            return
        if tag == 'style' and self.style_end is None and self.style_start is not None:
            self.style_end = self.getpos()[0]
            return
        if tag == 'head':
            self.head_end = self.getpos()[0]
            return
        if tag == 'body':
            self.body_end = self.getpos()[0]
            return

    def handle_data(self, data):
        extend_template = extends_regex.search(data)
        if extend_template and Path(extend_template.group('template')).suffix != '.sft':
            raise Exception('SFT can be used only within another SFT')
