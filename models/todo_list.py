from odoo import models, fields, api
from odoo.exceptions import ValidationError


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
    is_late = fields.Boolean()

    estimated_time = fields.Float(string='Estimated Time (hours)', required=True)
    timesheet_line_ids = fields.One2many('todo.timesheet.line', 'task_id', string='Timesheet Lines')

    @api.constrains('timesheet_line_ids')
    def _check_timesheet_total(self):
        for task in self:
            total_time = sum(line.hours for line in task.timesheet_line_ids)
            if total_time > task.estimated_time:
                raise ValidationError("Total time in timesheet lines cannot exceed the estimated time.")

    def action_close(self):
        for rec in self:
            rec.status = 'close'

    def check_overdue_tasks(self):
        overdue_tasks = self.search([('due_date', '<', fields.Date.today()), ('status', '!=', 'completed')])
        for task in overdue_tasks:
            task.is_late = True
