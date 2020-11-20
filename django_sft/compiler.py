import logging
import os
from pathlib import Path

from django.conf import settings
from django.template.loaders.app_directories import get_app_template_dirs

from django_sft.parser import TemplateParser
from django_sft.settings import GET_SCRIPT_TAG, GET_STYLE_TAG


logger = logging.getLogger(__name__)


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

    def prepare_script_tag(self, tag):
        lines = tag["lines"]
        # TODO Throw error if both "src" and "contents" are present
        if lines:
            contents = "\n".join(lines)
            # TODO The following line means that there can only be one <script>//js code...</script> per .sft file
            # If there are more, only the last one will be used
            with open(self.resulting_static_path.with_name("{}.js".format(self.resulting_static_path.stem)), 'w') as f:
                f.write(contents)
            script_tag = GET_SCRIPT_TAG(self.staticname)
        else:
            attrs = tag.get("attrs")
            html_attrs = " ".join(f'{key}="{value}"' for key, value in attrs)
            script_tag = f"<script {html_attrs}></script>"
        return script_tag

    def prepare_style_tag(self, tag):
        lines = tag["lines"]
        # TODO Throw error if both "src" and "contents" are present
        if lines:
            contents = "\n".join(lines)
            # TODO The following line means that there can only be one <style>//css code...</style> per .sft file
            # If there are more, only the last one will be used
            with open(self.resulting_static_path.with_name("{}.css".format(self.resulting_static_path.stem)), 'w') as f:
                f.write(contents)
            style_tag = GET_STYLE_TAG(self.staticname)
        else:
            attrs = tag.get("attrs")
            html_attrs = " ".join(f'{key}="{value}"' for key, value in attrs)
            html_attrs.replace("src=", "href=")
            style_tag = f"<link {html_attrs} />"
        return style_tag

    def get_script_tags(self, tags):
        return "\n".join([self.prepare_script_tag(tag) for tag in tags])

    def get_style_tags(self, tags):
        return "\n".join([self.prepare_style_tag(tag) for tag in tags])

    def compile_template(self, origin):
        # TODO This function should be cleaned up
        with open(origin) as f:
            contents = f.read()
        parser = TemplateParser()
        html, scripts, styles = parser.parse_sft(contents)
        # If no html is found, there is nothing to do here
        if not html:
            return

        # template_path = "app/templates/app/example.sft"
        templates_path = Path(origin)

        # TODO Should be able to control this with settings
        # self.resulting_templates_path = "app/templates/app/sft/example.sft"
        self.resulting_templates_path = templates_path.parent.joinpath('sft', templates_path.name)

        # TODO Should be able to control this with settings
        # self.resulting_static_path = "app/static/app/sft/example.sft"
        self.resulting_static_path = Path(*map(lambda x: x if x != 'templates' else 'static', self.resulting_templates_path.parts))

        # Create the resulting directories
        self.resulting_static_path.parent.mkdir(parents=True, exist_ok=True)
        self.resulting_templates_path.parent.mkdir(parents=True, exist_ok=True)

        # TODO Should be able to control this with settings
        # staticname = "app/sft/example"
        self.staticname = "/".join(self.resulting_static_path.parts[self.resulting_static_path.parts.index('static')+1:-1]) + f"/{self.resulting_static_path.stem}"

        # Add script and style tags
        style_tags_output = self.get_style_tags(styles)
        script_tags_output = self.get_script_tags(scripts)
        html_lines = html["lines"]
        if parser.head_end:
            # TODO The block name should be customizable
            style_tags_output += "\n{% block sft_style %}{% endblock sft_style %}"
            html_lines.insert(parser.head_end - 2, style_tags_output)
        elif html_lines:
            html_lines.append(f"{{% block sft_style %}}\n{style_tags_output}\n{{% endblock sft_style %}}")
        if parser.body_end:
            script_tags_output += "\n{% block sft_script %}{% endblock sft_script %}"
            html_lines.insert(parser.body_end - 1, script_tags_output)
        elif html_lines:
            html_lines.append(f"{{% block sft_script %}}\n{script_tags_output}\n{{% endblock sft_script %}}")

        if html_lines:
            with open(self.resulting_templates_path.with_name(f"{self.resulting_templates_path.stem}.html"), 'w') as f:
                f.write("\n".join(html_lines))


compiler = SFTCompiler()
def sft_compile():
    try:
        compiler.compile()
    except Exception as e:
        logger.exception(f"SFT compiling failed: {e}")
