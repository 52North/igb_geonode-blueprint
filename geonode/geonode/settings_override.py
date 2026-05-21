#
# Take the GeoNode settings documentation as a reference:
#
# https://docs.geonode.org/en/master/basic/settings/index.html#settings
#

import os
import ast
import sys


# sets defaults settings and from .env
from geonode.settings import *  # noqa
from geonode.settings import (  # noqa
    DEBUG,
    INSTALLED_APPS,
    SITEURL,
    TEMPLATES,
)

X_FRAME_OPTIONS = "SAMEORIGIN"
SECURE_CROSS_ORIGIN_OPENER_POLICY = None if DEBUG else "same-origin"


# relax origins for geonode-mapstore-client development
CSRF_TRUSTED_ORIGINS = (
    [
        "http://localhost",
    ]
    if DEBUG
    else ast.literal_eval(os.getenv("CSRF_TRUSTED_ORIGINS", "[]"))
)  # noqa
CORS_ALLOWED_ORIGINS = (
    [
        "http://localhost",
    ]
    if DEBUG
    else ast.literal_eval(os.getenv("CORS_ALLOWED_ORIGINS", "[]"))
)  # noqa
CORS_ALLOWED_ORIGIN_REGEXES = (
    [
        # match localhost with any port
        r"^http:\/\/localhost:*([0-9]+)?$",
        r"^https:\/\/localhost:*([0-9]+)?$",
    ]
    if DEBUG
    else ast.literal_eval(os.getenv("CORS_ALLOWED_ORIGIN_REGEXES", "[]"))
)  # noqa


STATIC_ROOT = "/mnt/volumes/statics/static/"
MEDIA_ROOT = "/mnt/volumes/statics/uploaded/"
ASSETS_ROOT = "/mnt/volumes/statics/assets/"


# Defines the directory that contains the settings file as the LOCAL_ROOT
# It is used for relative settings elsewhere.
LOCAL_ROOT = os.path.abspath(os.path.dirname(__file__))


# Additional directories which hold static files
# - Give priority to local ones
TEMPLATES[0]["DIRS"].insert(0, "/usr/src/geonode/templates")
loaders = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]
TEMPLATES[0]["OPTIONS"]["loaders"] = loaders
TEMPLATES[0].pop("APP_DIRS", None)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",  # noqa
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},  # noqa
    "handlers": {
        "console": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "simple",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "root": {
            "handlers": ["console"],
            "level": "WARNING",
        },
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "geonode": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "geoserver-restconfig.catalog": {
            "handlers": ["console"],
            "level": "ERROR",
        },
        "owslib": {
            "handlers": ["console"],
            "level": "ERROR",
        },
        "pycsw": {
            "handlers": ["console"],
            "level": "ERROR",
        },
        "celery": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "mapstore2_adapter.plugins.serializers": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "geonode_logstash.logstash": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}


INSTALLED_APPS += (
    "externalapplications",
    "customizations",
    #
    # Disabled because it's not working with v5
    #
    # Waiting for https://github.com/geosolutions-it/geonode-subsites/issues/47
    #
    #"subsites",
)

#
# App "subsites" is disabled because it's not working with v5
#
# Waiting for https://github.com/geosolutions-it/geonode-subsites/issues/47
#
# SUBSITE SPECIFIC CONFIGURATION
#ENABLE_SUBSITE_CUSTOM_THEMES = True
#ENABLE_CATALOG_HOME_REDIRECTS_TO = False
# return download_resourcebase and view resourcebase as permissions
#SUBSITE_READ_ONLY = False
# If TRUE will hide the `subsite_exclusive` resources also from the detailed endpoint `/documents`, `/maps`, `/datasets`, '/geoapps`
#SUBSITE_HIDE_EXCLUSIVE_FROM_SPECIFIC_API = True

#
# App "externalapplications"
#
EXTERNAL_APPLICATION_MENU_FILTER_AUTOCREATE = os.getenv('EXTERNAL_APPLICATION_MENU_FILTER_AUTOCREATE ', False)

#
#   Application proxy terminating SSL
#
if SITEURL.startswith("https"):
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

#
#   Remove, if https://github.com/GeoNode/geonode/pull/14143 is merged
#
# 100 MB
DEFAULT_MAX_UPLOAD_SIZE =  int(os.getenv("DEFAULT_MAX_UPLOAD_SIZE") or 100 * 1024 * 1024)
DEFAULT_MAX_PARALLEL_UPLOADS_PER_USER = int(os.getenv("DEFAULT_MAX_PARALLEL_UPLOADS_PER_USER") or 4)

if os.getenv("LDAP_ENABLED", "false").lower() == "true":
    #
    #   LDAP - https://github.com/GeoNode/geonode-contribs/tree/master/ldap
    #
    # ruff: disable[E402]
    from django_auth_ldap import config as ldap_config
    from geonode_ldap.config import GeonodeNestedGroupOfNamesType
    import ldap
    import json
    # ruff: enable[E402]

    # add geonode.contrib.ldap auth
    AUTHENTICATION_BACKENDS += (  # noqa: F405
        "geonode_ldap.backend.GeonodeLdapBackend",
    )

    def require_env(env_var_name):
        value = os.getenv(env_var_name)
        if not value:
            sys.stderr.write(f"CRITICAL CONFIG ERROR: Environment variable '{env_var_name}' is not configured!\n")
            sys.exit(1)
        return value

    # django_auth_ldap configuration
    AUTH_LDAP_SERVER_URI =require_env("LDAP_SERVER_URL")
    AUTH_LDAP_BIND_DN = require_env("LDAP_BIND_DN")
    AUTH_LDAP_BIND_PASSWORD = require_env("LDAP_BIND_PASSWORD")

    LDAP_USER_SEARCH_DN = require_env("LDAP_USER_SEARCH_DN")
    LDAP_USER_SEARCH_FILTERSTR = require_env("LDAP_USER_SEARCH_FILTERSTR")

    AUTH_LDAP_USER_SEARCH = ldap_config.LDAPSearch(
        LDAP_USER_SEARCH_DN,
        ldap.SCOPE_SUBTREE,
        LDAP_USER_SEARCH_FILTERSTR
    )

    ldap_user_attr_map_json = require_env("LDAP_USER_ATTR_MAP_JSON")
    try:
        AUTH_LDAP_USER_ATTR_MAP = json.loads(ldap_user_attr_map_json)
    except json.JSONDecodeError:
        sys.stderr.write(f"CRITICAL CONFIG ERROR: Environment variable 'LDAP_USER_ATTR_MAP_JSON' is not valid JSON!\n")
        sys.exit(1)

    ldap_always_update_user = require_env("LDAP_ALWAYS_UPDATE_USER")
    AUTH_LDAP_ALWAYS_UPDATE_USER = ldap_always_update_user.lower() == "true"

    try:
        AUTH_LDAP_CACHE_TIMEOUT = int(os.getenv("LDAP_CACHE_TIMEOUT", "3600"))
    except ValueError:
        sys.stderr.write(f"CRITICAL CONFIG ERROR: Environment variable 'LDAP_CACHE_TIMEOUT' is not valid integer!\n")
        sys.exit(1)

    auth_ldap_mirror_groups = require_env("LDAP_MIRROR_GROUPS")
    AUTH_LDAP_MIRROR_GROUPS = auth_ldap_mirror_groups.lower() == "true"

    if AUTH_LDAP_MIRROR_GROUPS:
        logger.debug("LDAP group features activated")

        LDAP_GROUP_SEARCH_DN = require_env("LDAP_GROUP_SEARCH_DN")
        AUTH_LDAP_GROUP_SEARCH = ldap_config.LDAPSearch(
            LDAP_GROUP_SEARCH_DN,
            ldap.SCOPE_SUBTREE,
        )

        AUTH_LDAP_GROUP_TYPE = GeonodeNestedGroupOfNamesType()

        ldap_mirror_groups_except = require_env("LDAP_MIRROR_GROUPS_EXCEPT")
        AUTH_LDAP_MIRROR_GROUPS_EXCEPT = [x.strip() for x in ldap_mirror_groups_except.split(",") if x.strip()]

        auth_ldap_find_group_perms = require_env("LDAP_FIND_GROUP_PERMS")
        AUTH_LDAP_FIND_GROUP_PERMS = auth_ldap_find_group_perms.lower() == "true"

        # geonode.contrib.ldap configuration
        GEONODE_LDAP_GROUP_NAME_ATTRIBUTE = require_env("LDAP_GROUP_NAME_ATTRIBUTE")
        GEONODE_LDAP_GROUP_PROFILE_FILTERSTR = require_env("LDAP_GROUP_PROFILE_FILTERSTR")
        GEONODE_LDAP_GROUP_PROFILE_MEMBER_ATTR = require_env("LDAP_GROUP_PROFILE_MEMBER_ATTR")
    else:
        logger.debug("LDAP group features NOT activated")
        AUTH_LDAP_MIRROR_GROUPS_EXCEPT = []
