from pathlib import Path

from django.template.loaders.app_directories import Loader


class SFTLoader(Loader):
    def get_template_sources(self, template_name):
        if template_name.endswith('.sft'):
            path = Path(template_name)
            path = path.parent.joinpath('sft', f"{path.stem}.html")
            return super().get_template_sources(str(path))
        else:
            return []
