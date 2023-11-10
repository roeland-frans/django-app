from setuptools import find_namespace_packages
from setuptools import setup

setup(
    name="app",
    packages=find_namespace_packages(),
    entry_points={"console_scripts": ["manage = app.manage:main"]},
    install_requires=[
        "black==23.11.0",
        "isort==5.12.0",
        "celery[redis]==5.3.4",
        "django-allow-cidr==0.7.1",
        "django-celery-beat==2.5.0",
        "django-celery-results==2.5.1",
        "django-cors-headers==4.3.0",
        "django-filter==23.3",
        "django-graphql-jwt==0.4.0",
        "django-storages[s3]==1.14.2",
        "Django==4.2.7",
        "email-validator==2.0.0",
        "graphene-django==3.1.5",
        "gunicorn==21.2.0",
        "psycopg==3.1.12",
        "pytest-django==4.1.0",
        "pytest==7.4.3",
    ],
)
