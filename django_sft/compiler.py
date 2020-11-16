import os
from pathlib import Path

from django.conf import settings
from django.template.loaders.app_directories import get_app_template_dirs

from django_sft.parser import TemplateParser
from django_sft.settings import GET_SCRIPT_TAG, GET_STYLE_TAG


class SFTCompiler(object):
    scripts = []
    styles = []

    def get_template_dirs(self):
        # TODO Should be able to control this with settings
        template_dir_list = get_app_template_dirs('templates')
        return list(template_dir_list) + list(settings.TEMPLATES[0]['DIRS'])

    def get_sft_templates(self):
        template_list = []
        for template_dir in (self.get_template_dirs()):
            for base_dir, dirnames, filenames in os.walk(template_dir):
                for filename in filenames:
                    if filename.endswith('.sft'):
                        template_list.append(os.path.join(base_dir, filename))

        return template_list

    def compile(self):
        templates = self.get_sft_templates()
        for template in templates:
            self.compile_template(template)

    def compile_template(self, origin):
        with open(origin) as f:
            contents = f.read()
        parser = TemplateParser()
        parser.feed(contents)
        lines = contents.split('\n')
        html = lines[parser.html_start:parser.html_end - 1] if parser.html_start else None
        script = lines[parser.script_start:parser.script_end - 1] if parser.script_start else None
        style = lines[parser.style_start:parser.style_end - 1] if parser.style_start else None

        templates = Path(origin)
        templates = templates.parent.joinpath('sft', templates.name)
        static = Path(*map(lambda x: x if x != 'templates' else 'static', templates.parts))
        static.parent.mkdir(parents=True, exist_ok=True)
        templates.parent.mkdir(parents=True, exist_ok=True)

        staticname = "/".join(static.parts[static.parts.index('static')+1:-1]) + f"/{static.stem}"

        script_tags = []
        style_tags = []

        if script:
            with open(static.with_name("{}.js".format(static.stem)), 'w') as f:
                f.write("\n".join(script))
            script_tag = GET_SCRIPT_TAG(staticname)
            script_tags.append(script_tag)

        if style:
            with open(static.with_name("{}.css".format(static.stem)), 'w') as f:
                f.write("\n".join(style))
            style_tag = GET_STYLE_TAG(staticname)
            style_tags.append(style_tag)

        # Add script and style tags
        style_tags_output = "\n".join(style_tags)
        script_tags_output = "\n".join(script_tags)
        if parser.head_end:
            style_tags_output += "{% block sft_style %}{% endblock sft_style %}"
            html.insert(parser.head_end - 2, style_tags_output)
        elif html:
            html.append(f"{{% block sft_style %}}{style_tags_output}{{% endblock sft_style %}}")
        if parser.body_end:
            script_tags_output += "{% block sft_script %}{% endblock sft_script %}"
            html.insert(parser.body_end - 1, script_tags_output)
        elif html:
            html.append(f"{{% block sft_script %}}{script_tags_output}{{% endblock sft_script %}}")


        if html:
            with open(templates.with_name(f"{templates.stem}.html"), 'w') as f:
                f.write("\n".join(html))


compiler = SFTCompiler()
def sft_compile():
    compiler.compile()
