# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from genweb6.ens.testing import GENWEB6_ENS_INTEGRATION_TESTING  # noqa: E501

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that genweb6.ens is properly installed."""

    layer = GENWEB6_ENS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if genweb6.ens is installed."""
        self.assertTrue(self.installer.is_product_installed(
            'genweb6.ens'))

    def test_browserlayer(self):
        """Test that IGenweb6EnsLayer is registered."""
        from genweb6.ens.interfaces import (
            IGenweb6EnsLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IGenweb6EnsLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = GENWEB6_ENS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstall_product('genweb6.ens')
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if genweb6.ens is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed(
            'genweb6.ens'))

    def test_browserlayer_removed(self):
        """Test that IGenweb6EnsLayer is removed."""
        from genweb6.ens.interfaces import \
            IGenweb6EnsLayer
        from plone.browserlayer import utils
        self.assertNotIn(IGenweb6EnsLayer, utils.registered_layers())
