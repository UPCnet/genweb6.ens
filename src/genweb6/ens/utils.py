# -*- coding: utf-8 -*-

from plone import api
from plone.memoize import ram
from plone.registry.interfaces import IRegistry
from zope.component import queryUtility
from zope.component import getMultiAdapter

from time import time

from genweb6.ens.controlpanels.ens import IEnsSettings


@ram.cache(lambda *args: time() // (24 * 60 * 60))
def genwebEnsConfig():
    registry = queryUtility(IRegistry)
    return registry.forInterface(IEnsSettings)


def get_portal_groups(view):
    acl_users = api.portal.get_tool("acl_users")
    return [group_id for group_id in acl_users.source_groups.getGroupIds()]


def get_user_groups(view):
    portal_state = getMultiAdapter(
        (view.context, view.request), name="plone_portal_state")
    if portal_state.anonymous():
        return set()
    elif not portal_state.member().getUser().getGroups():
        return set()
    else:
        return set(portal_state.member().getUser().getGroupIds())


def get_carpetes_vocabulary(view):
    """
    Get 3-level folders (genweb.ens.contenidor_ens actually)
    (e.g. gabinet-juridic in ens/ca/gabinet-juridic/) that match a portal group
    id. Return a list of tuples with the following structure:
      - index 0: path of the folder, e.g. /ens/ca/gabinet-juridic.
      - index 1: title of the folder, e.g. Gabinet Jurídic.
      - index 2: boolean representing whether the authenticated user belongs to
        the matched group.
    """
    portal_groups = get_portal_groups(view)
    user_groups = get_user_groups(view)
    catalog = api.portal.get_tool('portal_catalog')
    return [(folder.getPath(),
             folder.Title,
             folder.getPath().split('/')[-1] in user_groups)

            for folder in catalog.searchResults(
                portal_type='genweb.ens.contenidor_ens',
                sort_on='sortable_title')
            if folder.getPath().split('/')[-1] in portal_groups]
