# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict

from odoo import _, models
from odoo.exceptions import UserError

def _prepare_data(env, docids, data):
    # change product ids by actual product object to get access to fields in xml template
    # we needed to pass ids because reports only accepts native python types (int, float, strings, ...)

    layout_wizard = env['product.label.layout'].browse(data.get('layout_wizard'))
    if data.get('active_model') == 'product.template':
        Product = env['product.template'].with_context(display_default_code=False)
    elif data.get('active_model') == 'product.product':
        Product = env['product.product'].with_context(display_default_code=False)
    elif data.get("studio") and docids:
        # special case: users trying to customize labels
        products = env['product.template'].with_context(display_default_code=False).browse(docids)
        quantity_by_product = defaultdict(list)
        for product in products:
            quantity_by_product[product].append((product.barcode, 1))
        return {
            'quantity': quantity_by_product,
            'page_numbers': 1,
            'pricelist': layout_wizard.pricelist_id,
        }
    else:
        raise UserError(_('Product model not defined, Please contact your administrator.'))

    if not layout_wizard:
        return {}

    total = 0
    qty_by_product_in = data.get('quantity_by_product')
    # search for products all at once, ordered by name desc since popitem() used in xml to print the labels
    # is LIFO, which results in ordering by product name in the report
    products = Product.search([('id', 'in', [int(p) for p in qty_by_product_in.keys()])], order='name desc')
    quantity_by_product = defaultdict(list)
    for product in products:
        q = qty_by_product_in[str(product.id)]
        quantity_by_product[product].append((product.qr_code, q))
        total += q

    print({
        'quantity': quantity_by_product,
        'page_numbers': (total - 1) // (layout_wizard.rows * layout_wizard.columns) + 1,
        'price_included': data.get('price_included'),
        'extra_html': layout_wizard.extra_html,
        'pricelist': layout_wizard.pricelist_id,
    })

    return {
        'quantity': quantity_by_product,
        'page_numbers': (total - 1) // (layout_wizard.rows * layout_wizard.columns) + 1,
        'price_included': data.get('price_included'),
        'extra_html': layout_wizard.extra_html,
        'pricelist': layout_wizard.pricelist_id,
    }


class ReportProductTemplateLabelDymoQR(models.AbstractModel):
    _name = 'report.agproductqrcode.report_producttemplatelabel_dymo_qr'
    _description = 'Product Label QR Report'

    def _get_report_values(self, docids, data):
        return _prepare_data(self.env, docids, data)


class ReportProductTemplateLabel2x7(models.AbstractModel):
    _name = 'report.agproductqrcode.report_producttemplatelabel2x7_qr'
    _description = 'Product Label Report 2x7 QR'

    def _get_report_values(self, docids, data):
        return _prepare_data(self.env, docids, data)


class ReportProductTemplateLabel4x7Price(models.AbstractModel):
    _name = 'report.agproductqrcode.report_producttemplatelabel4x7_qr'
    _description = 'Product Label Report 4x7 Price QR'

    def _get_report_values(self, docids, data):
        return _prepare_data(self.env, docids, data)

class ReportProductTemplateLabel4x12(models.AbstractModel):
    _name = 'report.agproductqrcode.report_producttemplatelabel4x12_qr'
    _description = 'Product Label Report 4x12'

    def _get_report_values(self, docids, data):
        return _prepare_data(self.env, docids, data)


class ReportProductTemplateLabel4x12Price(models.AbstractModel):
    _name = 'report.agproductqrcode.report_producttemplatelabel4x12_price_qr'
    _description = 'Product Label Report 4x12 Price'

    def _get_report_values(self, docids, data):
        return _prepare_data(self.env, docids, data)