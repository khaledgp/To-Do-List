from odoo import models, fields

class TodoTask(models.Model):
    _name = 'todo.task'
    _description = 'Task for Todo List'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Task Name', required=True)
    assigned_to = fields.Many2one('res.partner', string='Assigned To', required=True)
    description = fields.Text(string='Description')
    due_date = fields.Date(string='Due Date')
    status = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('close', 'Close')
    ], string='Status', default='new')

    active = fields.Boolean(default=True)

    def action_close(self):
        for rec in self:
            rec.status = 'close'