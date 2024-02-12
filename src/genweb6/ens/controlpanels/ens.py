# -*- coding: utf-8 -*-
from Products.statusmessages.interfaces import IStatusMessage

from plone.app.registry.browser import controlpanel
from plone.autoform.directives import read_permission
from plone.autoform.directives import write_permission
from plone.dexterity.interfaces import IDexteritySchema
from plone.supermodel import model
from z3c.form import button
from zope import schema
from zope.ramcache import ram

from genweb6.ens import _


class IEnsSettings(model.Schema, IDexteritySchema):

    model.fieldset(
        'General',
        _(u'General'),
        fields=['url_info'])

    url_info = schema.TextLine(
        title=_(u"URL d'informació"),
        description=_(
            u"URL on enllaça la i de la barra superior del lloc web"),
        required=False,
    )

    model.fieldset(
        'Indicadors',
        _(u'Indicadors'),
        fields=['ws_endpoint', 'ws_key'],
    )

    ws_endpoint = schema.TextLine(
        title=_(u"URL del servei web"),
        required=False,
    )

    ws_key = schema.Password(
        title=_(u"API key del servei web"),
        required=False,
    )

    model.fieldset(
        'Migracio',
        _(u'Migracio'),
        fields=['enable_suscribers'])

    # MIGRACIO

    read_permission(enable_suscribers='genweb.webmaster')
    write_permission(enable_suscribers='genweb.manager')
    enable_suscribers = schema.Bool(
        title=_(u'Habilitar notificacions'),
        required=False,
        default=False,
    )
class EnsSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IEnsSettings
    label = _(u'Paràmetres de configuració de Genweb Ens')

    def updateFields(self):
        super(EnsSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(EnsSettingsEditForm, self).updateWidgets()

    def fix_password_fields(self, data):
        """
        Keep the stored value for the password fields not updated in the
        current request, i.e. those containing a None value.
        This method is needed since the password fields are not filled with
        their stored value when the edit form is loaded.
        """
        if not data['ws_key']:
            data['ws_key'] = self.getContent().ws_key

    @button.buttonAndHandler(_('Save'), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        self.fix_password_fields(data)
        self.applyChanges(data)
        ram.caches.clear()

        IStatusMessage(self.request).addStatusMessage(_("Changes saved"), "info")
        self.request.response.redirect(self.request.getURL())

    @button.buttonAndHandler(_("Cancel"), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_("Changes canceled."), "info")
        self.request.response.redirect(self.context.absolute_url() + '/' + self.control_panel_view)



class EnsSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = EnsSettingsEditForm
