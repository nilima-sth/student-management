{
    'name': 'SMS',
    'description': 'Student Management System',
    'sequence': -100,
    'version': '19.0.1.0.0',
    'summary': 'Manage student records and lifecycle',
    'category': 'Education',
    'license': 'LGPL-3',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/student_views.xml',
        'views/course_views.xml',
        'views/student_report_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
}