Django Single File Templates
============================

[![image](https://badge.fury.io/py/django-sft.svg)](https://badge.fury.io/py/django-sft)

[![image](https://travis-ci.org/zanderle/django-sft.svg?branch=master)](https://travis-ci.org/zanderle/django-sft)

[![image](https://codecov.io/gh/zanderle/django-sft/branch/master/graph/badge.svg)](https://codecov.io/gh/zanderle/django-sft)

Django Single File Templates \-- inspired by Vue\'s Single file
components

> Disclaimer: This package serves as a proof of concept rather than a production-ready solution!

Motivation
----------

From Vue\'s documentation:

> One important thing to note is that separation of concerns is not
> equal to separation of file types. In modern UI development, we have
> found that instead of dividing the codebase into three huge layers
> that interweave with one another, it makes much more sense to divide
> them into loosely-coupled components and compose them. Inside a
> component, its template, logic and styles are inherently coupled, and
> collocating them actually makes the component more cohesive and
> maintainable.

Similar logic could be applied to Django\'s templates. HTML, JavaScript
and CSS are inherently coupled so it makes sense to put them together.

Introducing **Django Single File Templates (SFT)**.

Quickstart
----------

Install Django Single File Templates:

    pip install django-sft

Add it to your \`INSTALLED\_APPS\`:

```python
INSTALLED_APPS = (
    ...
    'django_sft',
    ...
)
```

Add SFT Template loader (in your settings.py):

```python
TEMPLATES = [
    {
        ...
        'OPTIONS': {
            'loaders': [
                'django_sft.template.SFTLoader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            ...
        }
    }
]
```

You can now start using Single file templates as your templates.

Usage
-----

Add a new SFT by adding a `.sft` file to your `templates` folder (either
in your apps or root templates folder). SFT should include at least HTML
(you can use Django\'s template language), but it can also include
script and style tags:

```html
<template>
{% load static %}
<html lang=\"en\">
    <head>
        <meta charset=\"UTF-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
        <title>Example Website</title>
    </head>
    <body>
        <header>
            <nav>
                <a href=\"/\">Home</a>
                <a href=\"/page\" id=\"page\">Page</a>
            </nav>
        </header>
        {% block main %}
        <h1>This is where the content will go</h1>
        {% endblock %}
    </body>
</html>
</template>
<script>
const page = document.getElementById('page');
page.addEventListener('click', (ev) => {
  ev.preventDefault();
  alert('You clicked the page');
});
</script>

<style>
body {
  background-color: gray;
}
</style>
```

In your views you can render this template directly and SFT Template
loader will get the right template for you.

```python
def view(request):
return render('my-template.sft')}
```

Single file templates can also extend other STFs.

```html
<template>
{% extends 'example/base.sft' %}}
{% block main %}
    <h1>This is index page</h1>
    <h2>Update</h2>
    <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit eaque obcaecati maxime eos inventore tenetur, debitis atque quaerat modi, et illum id error quisquam consequatur reprehenderit, laboriosam exercitationem, provident aut.</p>

    <h2 id="time"></h2>
{% endblock %}
</template>

<script>
document.getElementById('time').innerHTML = new Date();
</script>

<style>
p {
    width: 50%;
    background-color: white;
    margin: auto;
}
</style>
```

Single file templates will automatically be parsed and compiled when you
`manage.py runserver` if `DEBUG = True`. You can also run
`manage.py compile_sft` to compile manually.

How does it work?
-----------------

When SFT is compiled (on `runserver` or manually), django-sft will grab
the SFT file and produce appropriate `.js`, `.css` and `.html` files.
They will be created in `sft` directory (under `static` and `templates`
directories respectively). The html files will be automatically injected
with references to the static files. When a view will try to render
`.sft` template, the SFT Template Loader will look for resulting `.html`
file instead and return that.

The current implementation is quite simple and serves as a proof of
concept rather than a production-ready solution.

Look for a working example under [tests folder](tests).

Features
--------

-   TODO

Running Tests
-------------

-   TODO: no tests written yet

Does the code actually work?

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

-   [Cookiecutter](https://github.com/audreyr/cookiecutter)
-   [cookiecutter-djangopackage](https://github.com/pydanny/cookiecutter-djangopackage)
