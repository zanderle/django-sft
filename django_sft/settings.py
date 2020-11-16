from django.conf import settings


def get_script_tag(templatename):
    return f"""<script src="{{% static '{templatename}.js'%}}"></script>"""

def get_style_tag(templatename):
    return f"""<link rel="stylesheet" href="{{% static '{templatename}.css'%}}"></link>"""


GET_SCRIPT_TAG = getattr(settings, 'GET_SCRIPT_TAG', get_script_tag)
GET_STYLE_TAG = getattr(settings, 'GET_STYLE_TAG', get_style_tag)
