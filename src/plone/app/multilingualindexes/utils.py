# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import safe_hasattr
from plone import api
from zope.schema._bootstrapinterfaces import ValidationError
import json


def get_configuration(request):
    try:
        return request.plone_app_multilingualindexes_fallbacks
    except AttributeError:
        fallbacks = json.loads(api.portal.get_registry_record(
            'multilingualindex.fallback_languages'))
        setattr(request, 'plone_app_multilingualindexes_fallbacks', fallbacks)
        return fallbacks


class JsonError(ValidationError):
    pass


def validate_fallback_record_change(event_or_data):
    if safe_hasattr(event_or_data, 'record'):
        if (event_or_data.record.__name__ !=
                'multilingualindex.fallback_languages'):
            return
        value_to_check = event_or_data.newValue
    else:
        value_to_check = event_or_data

    try:
        json.loads(value_to_check)
        return True
    except ValueError, e:
        raise JsonError(str(e))