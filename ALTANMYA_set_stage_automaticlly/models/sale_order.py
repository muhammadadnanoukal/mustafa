from odoo import api, fields, models,_
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def unlink(self):
        if self.opportunity_id:
            self.opportunity_id.set_stage()
        res = super().unlink()
        return res

    @api.model_create_multi
    def create(self, vals_list):
        res = super(SaleOrder, self).create(vals_list)
        for order in res:
            if order.opportunity_id:
                order.opportunity_id.set_stage('sales_status','draft')
        return res

    def write(self, vals):
        res = super().write(vals)
        if vals.get('state',False) and self.opportunity_id:
            if vals.get('state',False)!= 'cancel':
                state = vals.get('state')
                state = 'tentative approval' if state =='final approval' else state
                self.opportunity_id.set_stage('sales_status', state)
            else:
                production_ids = self.env['mrp.production'].search(
                    [('id', 'in', self.mrp_production_ids.ids), ('state', 'not in', ['draft', 'cancel'])])
                # check if there is an production order in progress related by this sale order
                if production_ids:
                    raise ValidationError(_(
                        "There is one or more production order called from this sale order\n"
                        "Please, cancel production order before cancel operation"))
                self.opportunity_id.set_stage()

        return res