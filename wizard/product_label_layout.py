# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError
import base64
import qrcode
from io import BytesIO


class ProductLabelLayout(models.TransientModel):
    _inherit = 'product.label.layout'

    def _prepare_report_data(self):
        xml_id, data = super(ProductLabelLayout, self)._prepare_report_data()
        if 'qr_code' in self.env.context and self.env.context.get('qr_code'):
            if self.print_format == 'dymo':
                xml_id = 'agproductqrcode.report_product_template_label_dymo_qr'
            if self.print_format == '2x7xprice':
                xml_id = 'agproductqrcode.report_product_template_label_2x7price_qr'
            if self.print_format == '4x7xprice':
                xml_id = 'agproductqrcode.report_product_template_label_4x7price_qr'
            if self.print_format == '4x12':
                xml_id = 'agproductqrcode.report_product_template_label_4x12_qr'
            if self.print_format == '4x12xprice':
                xml_id = 'agproductqrcode.report_product_template_label_4x12_price_qr'
        return xml_id, data

