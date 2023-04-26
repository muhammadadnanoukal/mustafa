from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def write(self, vals):
        res = super(StockPicking, self).write(vals)

        for record in self:
            print("write pick ", record.picking_type_id.code)
            print("has thes ", self.group_id.mrp_production_ids, self.group_id.sale_id)
            if record.state == 'done':
                if record.picking_type_id.code == 'internal':
                    for mo in self.group_id.mrp_production_ids:

                        sale_orders = mo.procurement_group_id.mrp_production_ids.move_dest_ids.group_id.sale_id
                        for order in sale_orders:
                            if order.opportunity_id:
                                order.opportunity_id.set_stage('operation_type_manufacturing', record.picking_type_id)
                if record.picking_type_id.code == 'outgoing':
                    for so in self.group_id.sale_id:
                        if so.opportunity_id:
                            so.opportunity_id.set_stage('operation_type_sales', record.picking_type_id)
        return

class ImmediateStockPicking(models.TransientModel):
    _inherit = "stock.immediate.transfer"


class StockBackOrderConfirmation1(models.TransientModel):
    _inherit = "stock.backorder.confirmation"