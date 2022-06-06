# -*- coding: utf-8 -*-
##############################################################################
#
#    SLTECH ERP SOLUTION
#    Copyright (C) 2020-Today(www.slecherpsolution.com).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import models, fields, api, _
from datetime import datetime, date, timedelta
import logging

_logger = logging.getLogger(__name__)


class PartnerXlsxoiu7(models.AbstractModel):
    _name = 'report.sltech_menu_popup.print_sample_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, obj):

        print(obj.from_date)
        print(obj.to_date)
        line_index = 3
        if obj.from_date and obj.to_date:
            cust_inv = [('date_order', '>=', str(obj.from_date)),
                         ('date_order', '<=', str(obj.to_date))]
            if obj.user_id:
                cust_inv.append(('user_id', '=', obj.user_id.id))
            if obj.config_id:
                cust_inv.append(('config_id', '=', obj.config_id.id))
            pos_order_ids = self.env['pos.order'].sudo().search(cust_inv)
            print(pos_order_ids)


        self = self.with_context(lang=self.env.user.lang)
        worksheet = workbook.add_worksheet()
        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 32)
        worksheet.set_column('C:C', 18)
        worksheet.set_column('D:D', 12)
        worksheet.set_column('E:E', 45)
        worksheet.set_column('F:F', 16)
        worksheet.set_column('G:G', 16)
        worksheet.set_column('H:H', 10)
        worksheet.set_column('I:I', 25)
        cell_format = workbook.add_format({'align': 'center', 'bold': 1,'bg_color':'#d8d8d8','border': 1,})
        format1 = workbook.add_format({'border': 1,'align': 'center',})
        worksheet.merge_range('E1:F1',_('Sales report from {'+str(obj.from_date)+'} to {'+str(obj.to_date)+'}'),cell_format)
        worksheet.write('A2', _('POS shop name'),cell_format)
        worksheet.write('B2', _('Order number'),cell_format)
        worksheet.write('C2', _('Date and time'),cell_format)
        worksheet.write('D2', _('Cashier'),cell_format)
        worksheet.write('E2', _('Product'),cell_format)
        worksheet.write('F2', _('Unit price w/o tax'),cell_format)
        worksheet.write('G2', _('Price after tax'),cell_format)
        worksheet.write('H2', _('Quantity'),cell_format)
        worksheet.write('I2', _('Total Price'),cell_format)

        for order in pos_order_ids:
            for lines in order.lines:

                temp_tax_amt = 0
                for tx_id in lines.tax_ids_after_fiscal_position:
                    tax_amt = tx_id.compute_all(lines.price_unit, order.currency_id, lines.qty, product=lines.product_id)
                    temp_tax_amt += sum(tax.get('amount', 0.0) for tax in tax_amt['taxes'])

                worksheet.write('A%s' % line_index, (order.config_id.name or ''),format1)
                worksheet.write('B%s' % line_index, (order.sltech_global_name or ''),format1)
                worksheet.write('C%s' % line_index, (str(order.date_order) or ''),format1)
                worksheet.write('D%s' % line_index, (order.user_id.name or ''),format1)
                worksheet.write('E%s' % line_index, (lines.full_product_name or ''),format1)
                worksheet.write('F%s' % line_index, (lines.price_subtotal or '0'),format1)
                worksheet.write('G%s' % line_index, (lines.price_subtotal_incl or '0'),format1)
                worksheet.write('H%s' % line_index, (lines.qty or '0'),format1)
                worksheet.write('I%s' % line_index, (lines.price_subtotal_incl or '0'),format1)
                line_index +=1
        amount_tax = sum(pos_order_ids.mapped('amount_tax'))
        amount_total = sum(pos_order_ids.mapped('amount_total'))
        amount_untaxed = amount_total - amount_tax
        worksheet.merge_range('A%s:B%s'%(line_index, line_index), _('Number of Orders'), cell_format)
        worksheet.write('C%s' % line_index,'' ,cell_format)
        worksheet.write('D%s' % line_index,'' ,format1)
        worksheet.write('E%s' % line_index,'' ,format1)
        worksheet.write('F%s' % line_index,'' ,format1)
        worksheet.write('G%s' % line_index,'' ,format1)
        worksheet.write('H%s' % line_index,'' ,format1)
        worksheet.write('I%s' % line_index, len(pos_order_ids), cell_format)
        line_index += 1
        worksheet.merge_range('A%s:B%s'%(line_index, line_index), _('Total before tax'), cell_format)
        worksheet.write('C%s' % line_index, '', cell_format)
        worksheet.write('D%s' % line_index, '', format1)
        worksheet.write('E%s' % line_index, '', format1)
        worksheet.write('F%s' % line_index, '', format1)
        worksheet.write('G%s' % line_index, '', format1)
        worksheet.write('H%s' % line_index, '', format1)
        worksheet.write('I%s' % line_index, amount_untaxed, cell_format)

        line_index += 1
        worksheet.merge_range('A%s:B%s'%(line_index, line_index), _('Tax'), cell_format)
        worksheet.write('C%s' % line_index, '', cell_format)
        worksheet.write('D%s' % line_index, '', format1)
        worksheet.write('E%s' % line_index, '', format1)
        worksheet.write('F%s' % line_index, '', format1)
        worksheet.write('G%s' % line_index, '', format1)
        worksheet.write('H%s' % line_index, '', format1)
        worksheet.write('I%s' % line_index, amount_tax, cell_format)

        line_index += 1
        worksheet.merge_range('A%s:B%s'%(line_index, line_index), _('Total including tax'), cell_format)
        worksheet.write('C%s' % line_index, '', cell_format)
        worksheet.write('D%s' % line_index, '', format1)
        worksheet.write('E%s' % line_index, '', format1)
        worksheet.write('F%s' % line_index, '', format1)
        worksheet.write('G%s' % line_index, '', format1)
        worksheet.write('H%s' % line_index, '', format1)
        worksheet.write('I%s' % line_index, amount_total, cell_format)


