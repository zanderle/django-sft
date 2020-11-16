=====
Usage
=====

To use Django Single File Templates in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_sft.apps.DjangoSftConfig',
        ...
    )

Add Django Single File Templates's URL patterns:

.. code-block:: python

    from django_sft import urls as django_sft_urls


    urlpatterns = [
        ...
        url(r'^', include(django_sft_urls)),
        ...
    ]
