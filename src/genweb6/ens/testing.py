# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE

from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import genweb6.ens


class Genweb6EnsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=genweb6.ens)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'genweb6.ens:default')


GENWEB6_ENS_FIXTURE = Genweb6EnsLayer()


GENWEB6_ENS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(GENWEB6_ENS_FIXTURE,),
    name='Genweb6EnsLayer:IntegrationTesting',
)


GENWEB6_ENS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(GENWEB6_ENS_FIXTURE,),
    name='Genweb6EnsLayer:FunctionalTesting',
)


GENWEB6_ENS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        GENWEB6_ENS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='Genweb6EnsLayer:AcceptanceTesting',
)
