# -*- coding: utf-8 -*-
{
    'name': "SK odoo Product QR Code",
    'summary': """
        Create Product With QR Code""",
    'description': """
        Create Product With QR Code
            """,
    'author': 'Sritharan K',
    'company': 'SKengineer',
    'maintainer': 'SKengineer',
    'website': "https://www.skengineer.be/",
    'category': 'Tools',
    'version': '17.1',
    'depends': ['base_setup', 'product'],
    'data': [
        'data/sequence.xml',
        'security/ir.model.access.csv',
        'security/group.xml',

        'report/product_report.xml',
        'report/product_template_template.xml',

        'views/res_config_setting_view.xml',
        'views/product_product_view.xml',
        'views/product_template_view.xml',

        'wizard/wizard_generate_qr_code_view.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
    'images': ['static/description/qr_code.png']
}
