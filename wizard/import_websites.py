# -*- coding: UTF-8 -*-
'''
    magento-integration

    :copyright: (c) 2013 by Openlabs Technologies & Consulting (P) LTD
    :license: AGPLv3, see LICENSE for more details
'''
import xmlrpclib
import socket

import ..api import Core
from openerp.osv import osv
from openerp.tools.translate import _


class ImportWebsites(osv.TransientModel):
    "Import websites from magentp"
    _name = 'magento.instance.import_websites'
    _description = __doc__

    def default_get(self, cursor, user, fields, context):
        """Set a default state

        :param cursor: Database cursor
        :param user: ID of current user
        :param fields: List of fields on wizard
        :param context: Application context
        """
        self.import_websites(cursor, user, context)
        return {}

    def import_websites(self, cursor, user, context):
        """Import the websites and their stores/view from magento

        :param cursor: Database cursor
        :param user: ID of current user
        :param context: Application context
        """
        Pool = self.pool

        instance_obj = Pool.get('magento.instance')

        for instance in instance_obj.browse(
            cursor, user, context.get('active_ids'), context
        ):
            try:
                with magento.Core(
                    instance.url, instance.api_user, instance.api_key
                ) as core_api:
                    websites = core_api.websites()
                    # Create websites, stores and store views
            except (
                xmlrpclib.Fault, IOError,
                xmlrpclib.ProtocolError, socket.timeout
            ):
                raise osv.except_osv(
                    _('Incorrect API Settings!'),
                    _('Please check and correct the API settings on instance.')
                )

ImportWebsites()
