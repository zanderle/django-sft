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
        self.scripts = []
        self.styles = []
        self.head_end = None
        self.body_end = None

    def handle_starttag(self, tag, attrs):
        if tag == 'template' and self.html_start is None:
            self.html_start = self.getpos()
            return
        if tag == 'script' and self.html_end is not None:
            self.scripts.append({'start': self.getpos(), 'attrs': attrs})
            return
        if tag == 'style' and self.html_end is not None:
            self.styles.append({'start': self.getpos(), 'attrs': attrs})
            return

    def handle_endtag(self, tag):
        if tag == 'template' and self.html_end is None:
            self.html_end = self.getpos()
            return
        if tag == 'script' and self.html_end is not None:
            if 'end' in self.scripts[-1]:
                raise Exception("end tag registered twice")
            self.scripts[-1]['end'] = self.getpos()
            return
        if tag == 'style' and self.html_end is not None:
            if 'end'  in self.styles[-1]:
                raise Exception("end tag registered twice")
            self.styles[-1]['end'] = self.getpos()
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

    def get_contents(self, tag):
        start = tag["start"][0]
        end = tag["end"][0]
        attrs = tag.get("attrs", [])
        return {
            "lines": self.lines[start:end-1],
            "attrs": attrs
        }

    def parse_sft(self, sft_template):
        self.feed(sft_template)
        self.lines = sft_template.split('\n')

        if self.html_start and self.html_end:
            html = self.get_contents({"start": self.html_start, "end": self.html_end})
            scripts = [self.get_contents(script) for script in self.scripts]
            styles = [self.get_contents(style) for style in self.styles]

            return html, scripts, styles

        else:
            return None, None, None
