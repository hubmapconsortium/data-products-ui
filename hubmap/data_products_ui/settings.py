"""
Django settings for data_products_ui project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import json
import sys
from os import fspath
from pathlib import Path
from subprocess import run

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# !!! for development, overridden in `production_settings.py` by Docker container build

SECRET_KEY = "django-insecure-fbrbads+f1&s^#x(o-s#ce0+0gzdx^!!fv_@ht8mp2ut(lt9ux"

DEBUG = True

ALLOWED_HOSTS = ["*"]

# /!!! for development, overridden in `production_settings.py` by Docker container build

# Application definition

INSTALLED_APPS = [
    "data_products.apps.DataProductsConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "data_products",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "data_products_ui.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "data_products_ui.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "db",
        "PORT": 5432,
    },
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

VERSION_PATHS = [
    Path("/opt/data-products-ui/version.json"),
    Path("/code/version.json"),
]


def get_app_version() -> str:
    try:
        p = run(["git", "describe", "--always", "--abbrev=12", "--dirty"], capture_output=True)
        if not p.returncode:
            return p.stdout.decode().strip()
    except FileNotFoundError:
        # no 'git' executable in prod image
        pass

    for version_path in VERSION_PATHS:
        if version_path.is_file():
            with open(version_path) as f:
                return json.load(f)["version"]

    return "unknown"


APP_VERSION = get_app_version()

# Keep this as the last section of this file!
try:
    from .local_settings import *
except ImportError:
    pass
# Intended to be a temporary hack for overriding settings in production.
# TODO: figure out a better way to do this, probably with a different path
override_settings_file = Path("/opt/secret/override_settings.py")
if override_settings_file.is_file():
    print("Reading production override settings from", override_settings_file)
    sys.path.append(fspath(override_settings_file.parent))
    try:
        from override_settings import *
    except ImportError as e:
        print("Couldn't read override settings found at", override_settings_file)
        raise
# Sometimes we do need to define settings in terms of other settings, so
# this is a good place to do so, after override settings are loaded.
# Shouldn't define any constants at this point though

# !!! overrides that depend on other (including local) settings

# (none yet)

# /!!! overrides that depend on other (including local) settings

# Do not add anything after this
