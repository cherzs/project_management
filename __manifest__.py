{
    'name': 'Project Management',
    'version': '1.0',
    'depends': ['base', 'web', 'mail', 'rating', 'project'],
    'author': 'Cherzs',
    'sequence': -1,
    'category': 'Project Management',
    'description': ''' A simple project management module''',
    'data': [
        'security/ir.model.access.csv',
        'security/project_security.xml',
        'data/project_task_stage_data.xml',
        'views/project_views.xml',
        'views/task_views.xml',
        'views/menu.xml',
    ],
    'demo': [
        'data/project_management_demo.xml',
        'data/task_management_demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
        ],
    },
    'installable': True,
    'application': True,
}