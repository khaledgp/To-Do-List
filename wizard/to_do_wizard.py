from odoo import models, fields

class TodoTaskAssignWizard(models.TransientModel):
    _name = 'todo.task.assign.wizard'
    _description = 'Assign Tasks to Partner'

    task_ids = fields.Many2many('todo.task', string='Tasks', domain="[('status', 'not in', ['completed', 'close'])]")
    partner_id = fields.Many2one('res.partner', string='Assign To', required=True)

    def assign_tasks(self):
        for task in self.task_ids:
            task.write({'assigned_to': self.partner_id.id})
