# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName

from genweb6.core.indicators import RegistryException
from genweb6.core.indicators import ReporterException
from genweb6.core.indicators import WebServiceReporter
from genweb6.ens.utils import genwebEnsConfig
from genweb6.ens.indicators.registry import get_registry

import logging
import transaction

logger = logging.getLogger(name='genweb.ens')


def update_if_review_state(content, review_state):
    workflow_tool = getToolByName(content, 'portal_workflow')
    if workflow_tool.getInfoFor(content, 'review_state') in review_state:
        update(context=content)


def update(context):
    transaction.get().addAfterCommitHook(
        update_after_commit_hook,
        kws=dict(context=context))


def update_after_commit_hook(is_commit_successful, context):
    if not is_commit_successful:
        return
    try:
        ws_url = genwebEnsConfig('ws_endpoint')
        ws_key = genwebEnsConfig('ws_key')
        registry = get_registry(context)

        reporter = WebServiceReporter(ws_url, ws_key)
        reporter.report(registry)
        logger.info("Indicators were successfully reported")
    except RegistryException as e:
        logger.warning(
            "Error while loading indicator registry ({0})".format(e))
    except ReporterException as e:
        logger.warning("Error while reporting indicators ({0})".format(e))
