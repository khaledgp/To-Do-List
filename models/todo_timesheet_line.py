from odoo import models, fields


class TodoTimesheetLine(models.Model):
    _name = 'todo.timesheet.line'

    task_id = fields.Many2one('todo.task', string='Task', required=True)
    date = fields.Date(string='Date', required=True)
    hours = fields.Float(string='Hours', required=True)
    description = fields.Text(string='Description')
