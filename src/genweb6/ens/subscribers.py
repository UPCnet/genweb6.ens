# -*- coding: utf-8 -*-

from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes

from plone.dexterity.utils import createContentInContainer

from genweb6.ens.indicators.updating import update as update_indicators
from genweb6.ens.indicators.updating import update_if_review_state as update_indicators_if_review_state
from genweb6.ens.utils import genwebEnsConfig

def create_folder(container, id, title, addable_types):
    folder = createContentInContainer(
        container,
        "Folder",
        id=id,
        title=title,
        exclude_from_nav=True)
    folder_constraints = ISelectableConstrainTypes(folder)
    folder_constraints.setConstrainTypesMode(1)
    folder_constraints.setLocallyAllowedTypes(addable_types)
    folder_constraints.setImmediatelyAddableTypes(addable_types)


def initialize_ens(ens, event):

    ens_tool = genwebEnsConfig()
    if not ens_tool.enable_suscribers:
        return

    create_folder(
        ens,
        "altres-documents",
        "Altres documents",
        ('Document', 'File', 'Folder', 'Image', 'genweb.ens.document_interes'))

    create_folder(
        ens,
        "reunions",
        "Reunions",
        ('Document', 'File', 'Folder', 'Image', 'genweb.ens.acta_reunio'))


def update_indicators_on_ens_deletion(obj, event):

    ens_tool = genwebEnsConfig()
    if not ens_tool.enable_suscribers:
        return

    update_indicators_if_review_state(obj, ('intranet', 'published'))


def update_indicators_on_ens_review_state_change(obj, event):

    ens_tool = genwebEnsConfig()
    if not ens_tool.enable_suscribers:
        return

    update_indicators(context=obj)
