# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView


urlpatterns = [
    url(r'', TemplateView.as_view(template_name="example/index.sft")),
    url(r'^admin/', admin.site.urls),
]
