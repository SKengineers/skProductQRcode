# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import datetime


class WizardGenerateQRCode(models.TransientModel):
    _name = 'wizard.generate.qr.code'
    _description = "Generate QR Code"

    overwrite = fields.Boolean(string='Overwrite QR Code if Exists')
    model = fields.Char(string='Model')
    product_template_ids = fields.Many2many('product.template')
    product_product_ids = fields.Many2many('product.product')

    @api.model
    def default_get(self, fields):
        res = super(WizardGenerateQRCode, self).default_get(fields)
        if 'active_model' in self.env.context:
            res['model'] = self.env.context.get('active_model')
            if self.env.context.get('active_model') == 'product.template':
                res['product_template_ids'] = [(6, 0, self.env['product.template'].search([
                    ('id', 'in', self.env.context.get('active_ids'))
                ]).ids)]
            if self.env.context.get('active_model') == 'product.product':
                res['product_product_ids'] = [(6, 0, self.env['product.product'].search([
                    ('id', 'in', self.env.context.get('active_ids'))
                ]).ids)]
        return res

    def action_generate(self):
        if self.overwrite:
            for tmpl in self.product_template_ids:
                tmpl.qr_code = self.env['ir.sequence'].next_by_code('qr.code.product.template')
                tmpl.compute_qr_code_image()
            for pro in self.product_product_ids:
                pro.qr_code = self.env['ir.sequence'].next_by_code('qr.code.product.variant')
                pro.compute_qr_code_image()
        else:
            for tmpl in self.product_template_ids.filtered(lambda x: not x.qr_code):
                tmpl.qr_code = self.env['ir.sequence'].next_by_code('qr.code.product.template')
                tmpl.compute_qr_code_image()
            for pro in self.product_product_ids.filtered(lambda x: not x.qr_code):
                pro.qr_code = self.env['ir.sequence'].next_by_code('qr.code.product.variant')
                pro.compute_qr_code_image()