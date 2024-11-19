{
    'name': 'To Do List',
    'author':'Khaled GP',
    'version': '1.0',
    'category': '',
    'depends': ['base','web', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/sequence.xml',
        'views/base_menu.xml',
        'views/todo_list_views.xml',
        'reports/custom_header_footer.xml',
        'reports/todo_reports.xml',
        'wizard/to_do_wizard_view.xml',

    ],
    'application': True,
    'installable': True,
}
