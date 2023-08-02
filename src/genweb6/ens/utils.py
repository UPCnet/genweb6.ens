# -*- coding: utf-8 -*-

from plone.memoize import ram
from plone.registry.interfaces import IRegistry
from zope.component import queryUtility

from genweb6.ens.controlpanels.ens import IEnsSettings


@ram.cache(lambda *args: time() // (24 * 60 * 60))
def genwebEnsConfig():
    registry = queryUtility(IRegistry)
    return registry.forInterface(IEnsSettings)