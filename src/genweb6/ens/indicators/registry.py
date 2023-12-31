# -*- coding: utf-8 -*-

"""
Registry containing the indicators that will be updated on the Indicators WS.
"""

from genweb6.core.indicators import Registry
from genweb6.core.indicators import RegistryException

import logging
import os


logger = logging.getLogger(name='genweb.ens')

registry = None
registry_initialized = False


def initialize(context):
    global registry_initialized
    if not registry_initialized:
        register(context)
        registry_initialized = True


def get_registry(context):
    initialize(context)
    return registry


def register(context):
    global registry

    definitions_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'definitions')
    registry = Registry(context)
    registry.load_from_path(definitions_path)
    logger.info(
        "Indicators successfully loaded from {0}".format(definitions_path))
