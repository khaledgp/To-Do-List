from odoo import models, fields

class TodoTask(models.Model):
    _name = 'todo.task'
    _description = 'Task for Todo List'

    name = fields.Char(string='Task Name', required=True)
    assigned_to = fields.Many2one('res.partner', string='Assigned To', required=True)
    description = fields.Text(string='Description')
    due_date = fields.Date(string='Due Date')
    status = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ], string='Status', default='new')
