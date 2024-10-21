# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError
import base64
import qrcode
from io import BytesIO


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    qr_code = fields.Char(string='QR Code')
    qr_code_image = fields.Binary(string='QR Code Image', compute='compute_qr_code_image', store=True)

    @api.depends('qr_code')
    def compute_qr_code_image(self):
        for product in self:
            if product.qr_code:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                )
                data = product.qr_code
                qr.add_data(data)
                qr.make(fit=True)

                img = qr.make_image(fill_color="black", back_color="white")
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue())
                product.qr_code_image = img_str
            else:
                product.qr_code_image = False

    @api.model_create_multi
    def create(self, vals_list):
        res = super(ProductTemplate, self).create(vals_list)
        auto_create_qr_code = self.env['ir.config_parameter'].get_param('agproductqrcode.create_automatically_qr_code')
        print(self.env.user.has_group('agproductqrcode.group_qr_code_generator'))
        print(auto_create_qr_code)
        if self.env.user.has_group('agproductqrcode.group_qr_code_generator') and auto_create_qr_code:
            for rec in res:
                if not rec.qr_code:
                    rec.qr_code = self.env['ir.sequence'].next_by_code('qr.code.product.template')
                    rec.compute_qr_code_image()
        return res

    def action_open_label_qr_layout(self):
        action = self.env['ir.actions.act_window']._for_xml_id('product.action_open_label_layout')
        action['context'] = {'default_product_tmpl_ids': self.ids, 'qr_code': True}
        return action