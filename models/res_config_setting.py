# -*- coding:utf-8 -*-
from odoo import fields, models, api, _, Command


class ResConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    create_automatically_qr_code = fields.Boolean(string='Is Generate QR Code When Product Create?', help="Is Generate QR Code When Product Create?")

    @api.model
    def get_values(self):
        """get values from the fields"""
        res = super(ResConfigSetting, self).get_values()
        res.update(
            create_automatically_qr_code=self.env['ir.config_parameter'].sudo().get_param('agproductqrcode.create_automatically_qr_code')
        )
        return res

    def set_values(self):
        super(ResConfigSetting, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('agproductqrcode.create_automatically_qr_code', self.create_automatically_qr_code)