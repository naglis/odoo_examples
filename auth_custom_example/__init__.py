# Copyright 2018 Naglis Jonaitis
# License LGPL-3 or later (https://www.gnu.org/licenses/lgpl).

from odoo import SUPERUSER_ID, exceptions, http, models, tools
from odoo.http import request


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _auth_method_custom(cls):
        auth_header = request.httprequest.headers.get('Authorization')
        if auth_header and tools.consteq(auth_header, '42'):
            if not request.session.uid:
                request.uid = SUPERUSER_ID
            # Valid user session exists, decide what to do here.
            else:
                request.uid = request.session.uid
        else:
            raise exceptions.AccessDenied()


class Controller(http.Controller):

    @http.route('/custom_auth/test', type='json', auth='custom')
    def custom_auth_test(self):
        return {
            'uid': request.uid,
        }
