# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT

class POSOrder(models.Model):
    _inherit = "pos.order"

    sltech_global_name = fields.Char('Global Sequence', readonly=True)

    @api.model
    def create(self, vals):
        vals['sltech_global_name'] = self.env['ir.sequence'].next_by_code('global.pos.sequence') or _('New')
        return super(POSOrder, self).create(vals)

    @api.model
    def create_from_ui(self, orders, draft=False):
        """ Create and update Orders from the frontend PoS application.

        Create new orders and update orders that are in draft status. If an order already exists with a status
        diferent from 'draft'it will be discareded, otherwise it will be saved to the database. If saved with
        'draft' status the order can be overwritten later by this function.

        :param orders: dictionary with the orders to be created.
        :type orders: dict.
        :param draft: Indicate if the orders are ment to be finalised or temporarily saved.
        :type draft: bool.
        :Returns: list -- list of db-ids for the created and updated orders.
        """
        res = super(POSOrder, self).create_from_ui(orders, draft)
        return self.env['pos.order'].search_read(domain=[('id', 'in', [x['id'] for x in res])], fields=['id', 'pos_reference', 'sltech_global_name'])
