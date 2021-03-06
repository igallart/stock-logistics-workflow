# Copyright 2013-15 Agile Business Group sagl (<http://www.agilebg.com>)
# Copyright 2015-2016 AvanzOSC
# Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2017 Jacques-Etienne Baudoux <je@bcim.be>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    invoice_ids = fields.Many2many(
        comodel_name='account.invoice',
        copy=False,
        string='Invoices',
        readonly=True,
    )

    @api.multi
    def action_view_invoice(self):
        """This function returns an action that display existing invoices
        of given stock pickings.
        It can either be a in a list or in a form view, if there is only
        one invoice to show.
        """
        self.ensure_one()
        # Determine display out invoices views or in invoices views
        if (self.location_dest_id.usage == 'customer'
                or self.location_id.usage == 'customer'):
            action_name = 'account.action_invoice_tree1'
            form_view_name = 'account.invoice_form'
        else:
            action_name = 'account.action_invoice_tree2'
            form_view_name = 'account.invoice_supplier_form'

        action = self.env.ref(action_name)
        result = action.read()[0]
        if len(self.invoice_ids) > 1:
            result['domain'] = "[('id', 'in', %s)]" % self.invoice_ids.ids
        else:
            form_view = self.env.ref(form_view_name)
            result['views'] = [(form_view.id, 'form')]
            result['res_id'] = self.invoice_ids.id
        return result
