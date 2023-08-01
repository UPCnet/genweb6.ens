# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes

from plone import api
from plone import api
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.component import getUtility
from zope.interface import implementer

import csv
import logging
import os

data_folder_name = 'data'
consell_direccio_file_name = 'consell_direccio.csv'

PROFILE_ID = 'profile-genweb6.ens:default'

INDEXES = (('estat', 'FieldIndex'),
           ('figura_juridica', 'FieldIndex'),
           ('dni', 'FieldIndex'),
           ('carrec', 'FieldIndex'),
           ('is_historic', 'FieldIndex'),
           ('data', 'DateIndex'),
           ('is_vigent', 'FieldIndex'),
           ('organ', 'FieldIndex'),
           ('tipus', 'FieldIndex'))


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "genweb6.ens:uninstall",
        ]

    def getNonInstallableProducts(self):
        """Hide the upgrades package from site-creation and quickinstaller."""
        return ["genweb6.ens.upgrades"]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


# Afegit creació d'indexos programàticament i controladament per:
# http://maurits.vanrees.org/weblog/archive/2009/12/catalog
def add_catalog_indexes(context, logger=None):
    """Method to add our wanted indexes to the portal_catalog.

    @parameters:

    When called from the import_various method below, 'context' is
    the plone site and 'logger' is the portal_setup logger.  But
    this method can also be used as upgrade step, in which case
    'context' will be portal_setup and 'logger' will be None.
    """
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger(__name__)

    # Run the catalog.xml step as that may have defined new metadata
    # columns.  We could instead add <depends name="catalog"/> to
    # the registration of our import step in zcml, but doing it in
    # code makes this method usable as upgrade step as well.  Note that
    # this silently does nothing when there is no catalog.xml, so it
    # is quite safe.
    setup = api.portal.get_tool(name='portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'catalog')

    catalog = api.portal.get_tool(name='portal_catalog')
    indexes = catalog.indexes()

    indexables = []
    for name, meta_type in INDEXES:
        if name not in indexes:
            catalog.addIndex(name, meta_type)
            indexables.append(name)
            logger.info('Added %s for field %s.', meta_type, name)
    if len(indexables) > 0:
        logger.info('Indexing new indexes %s.', ', '.join(indexables))
        catalog.manage_reindexIndex(ids=indexables)


def add_container(container, type, title,
                  allowed_types=None, exclude_from_nav=False):
    folder_id = getUtility(IIDNormalizer).normalize(title)
    if folder_id not in container:
        folder = api.content.create(
            type=type,
            id=folder_id,
            title=title,
            container=container)
        # api.content.transition(
        #     obj=folder,
        #     transition='reject')
        if allowed_types:
            behavior = ISelectableConstrainTypes(folder)
            behavior.setConstrainTypesMode(1)
            behavior.setLocallyAllowedTypes(allowed_types)
            behavior.setImmediatelyAddableTypes(allowed_types)
        folder.exclude_from_nav = exclude_from_nav
    return container[folder_id]


def add_representant_upc(folder, title, carrec):
    representant_id = getUtility(IIDNormalizer).normalize(title)
    if representant_id not in folder:
        representant = api.content.create(
            type='genweb.ens.representant',
            id=representant_id,
            title=title,
            container=folder,
            carrec=carrec)
        # api.content.transition(
        #     obj=folder,
        #     transition='reject')
    return folder[representant_id]


def add_representants_upc():
    portal = api.portal.get()
    if 'ca' in portal:
        representants_folder = add_container(
            container=portal['ca'],
            type='Folder',
            title=u"Representants UPC",
            exclude_from_nav=True)
        consell_direccio_folder = add_container(
            container=representants_folder,
            type='genweb.ens.contenidor_representants',
            title=u"Consell de Direcció")
        add_container(
            container=representants_folder,
            type='genweb.ens.contenidor_representants',
            title=u"Altres")

        consell_direccio_file_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            data_folder_name,
            consell_direccio_file_name)

        with open(consell_direccio_file_path, 'r') as consell_direccio_file:
            for row in csv.reader(consell_direccio_file,
                                  delimiter=',', quotechar='"'):
                add_representant_upc(
                    consell_direccio_folder,
                    title=row[1],
                    carrec=row[0])


def add_collections_folder():
    portal = api.portal.get()
    if 'ca' in portal:
        add_container(
            container=portal['ca'],
            type='Folder',
            title=u"Col·leccions",
            allowed_types=('Collection',),
            exclude_from_nav=True)


def add_predefined_data():
    add_representants_upc()
    add_collections_folder()


def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('genweb6.ens_various.txt') is None:
        return

    portal = context.getSite()
    logger = logging.getLogger(__name__)

    add_catalog_indexes(portal, logger)
    add_predefined_data()