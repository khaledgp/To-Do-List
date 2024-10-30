{
    'name': 'To Do List',
    'author':'Khaled GP',
    'version': '1.0',
    'category': '',
    'depends': ['base','web', 'mail'],
    'data': [
        'views/base_menu.xml',
        'views/todo_list_views.xml',
        'security/ir.model.access.csv',
        'reports/custom_header_footer.xml',
        'reports/todo_reports.xml',

    ],
    'application': True,
    'installable': True,
}
