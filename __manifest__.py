{
    'name': 'SMS',
    'description': 'Student Management System',
    'sequence': -100,
    'version': '19.0.1.0.0',
    'summary': 'Manage student records and courses efficiently.',
    'category': 'Education',
    'license': 'LGPL-3',
    'depends': ['base', 'contacts', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/course_views.xml',
        'views/student_views.xml',
        'views/student_report_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
}
