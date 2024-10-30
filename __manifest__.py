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
        'views/menu.xml',
        'views/project_views.xml',
        'views/task_views.xml',
        ],
    'demo':[
        'data/roject_management_demo.xml',
        'data/project_management_demo.xml'
        ],
    'assets': {
        'web.assets_backend': [
          
        ],
    },
    'installable': True,
    'application': True,
}