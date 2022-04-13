from odoo import models, api, fields, _
from datetime import datetime

class SaleOrder(models.TransientModel):
    _name = "inventory.wizard"
    _descripton = "Sales Excel Report"

    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    user_id = fields.Many2one('hr.employee',string='Cashier')
    config_id = fields.Many2one('pos.config',string='POS Shop')

    def generate_report_xlsx(self):
        return self.env.ref('sltech_menu_popup.sltech_pos_excel_report_invoice_xlsx_pos').report_action(self)

    def _sltech_get_report_filename(self):
        self = self.with_context(lang=self.env.user.lang)
        return _("Sales Excel Report "+str(datetime.now().date()))