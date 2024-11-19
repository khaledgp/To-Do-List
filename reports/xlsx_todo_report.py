from docutils.nodes import header
from ast import literal_eval
from odoo import http
from odoo.http import request
import io
import xlsxwriter

class XlsxTodoReport(http.Controller):
    @http.route('/todo/excel/report/<string:task_id>', type='http', auth='user')
    def download_exel_report_todo(self, task_id):

        task_id = request.env['todo.task'].browse(literal_eval(task_id))
        print(task_id)

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Tasks')

        header_format = workbook.add_format({'bold': True, 'bg_color': '#a2a2a2', 'border': 1, 'align': 'center'})
        string_format = workbook.add_format({'border': 1, 'align': 'center'})

        headers = ['Task Name', 'Assigned To', 'Description', 'Due Date', 'Status']
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header, header_format)

        row_num = 1
        for task in task_id:
            assigned_to_name = task.assigned_to.name if task.assigned_to else 'Unassigned'
            due_date = task.due_date.strftime('%Y-%m-%d') if task.due_date else 'No Due Date'

            worksheet.write(row_num, 0, task.name or 'No Name', string_format)
            worksheet.write(row_num, 1, assigned_to_name, string_format)
            worksheet.write(row_num, 2, task.description or 'No Description', string_format)
            worksheet.write(row_num, 3, due_date, string_format)
            worksheet.write(row_num, 4, task.status or 'No Status', string_format)
            row_num += 1

        workbook.close()
        output.seek(0)

        report_name = 'ToDo Report.xlsx'

        return request.make_response(
            output.getvalue(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', f'attachment; filename={report_name}')
            ]
        )
