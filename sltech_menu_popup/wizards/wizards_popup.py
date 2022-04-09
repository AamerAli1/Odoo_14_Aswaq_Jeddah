from odoo import models, api, fields, _


class SaleOrder(models.TransientModel):
    _name = "inventory.wizard"

    from_date = fields.Datetime(string='From Date')
    to_date = fields.Datetime(string='To Date')
    user_id = fields.Many2one('res.users',string='Cashier')
    config_id = fields.Many2one('pos.config',string='POS Shop')

    def generate_report_xlsx(self):
        return self.env.ref('sltech_menu_popup.sltech_pos_excel_report_invoice_xlsx_pos').report_action(self)


