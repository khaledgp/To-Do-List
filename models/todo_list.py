from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TodoTask(models.Model):
    _name = 'todo.task'
    _description = 'Task for Todo List'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ref = fields.Char(default='New', readonly=1)
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


    @api.model
    def create(self, vals):
        res = super(TodoTask, self).create(vals)
        if res.ref == 'New':
           res.ref = self.env['ir.sequence'].next_by_code('task_seq')

        return res

    def write(self, vals):
        for rec in self:
            if rec.status in ['completed', 'close']:
                raise ValidationError(f"Cannot modify a task that is {rec.status}.")
        return super(TodoTask, self).write(vals)


    def action_assign_tasks_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('todo_management.action_todo_task_assign_wizard')

        return action



    def print_xlsx_report(self):
        return {
            'type': 'ir.actions.act_url',
            'url': f'/todo/excel/report/{self.env.context.get("active_ids")}',
            'target': 'new'
        }