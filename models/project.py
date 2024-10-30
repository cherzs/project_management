from odoo import models, fields, api

class Project(models.Model):
    _name = 'project.management'
    _description = 'Project Management'
    _order = 'sequence, name'

    name = fields.Char(string='Project Name', required=True, tracking=True, index=True)
    user_id = fields.Many2one('res.users', string='Project Manager', tracking=True, index=True)
    date = fields.Datetime(string='Date', default=fields.Datetime.now)
    description = fields.Text(string='Description')
    date_start = fields.Datetime(string="Start Date")
    date_end = fields.Datetime(string="End Date")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', required=True, tracking=True)
    
    sequence = fields.Integer("Sequence", default=10)
    color = fields.Integer("Color")
    active = fields.Boolean(string='Active', default=True, index=True)
    partner_id = fields.Many2one('res.partner', string='Customer', index=True)
    is_favorite = fields.Boolean(string='Favorite', default=False)
    tag_ids = fields.Many2many('projects.tags', string='Tags')
    project_id = fields.Many2one('project.management', string='Project', required=True, tracking=True)

    
    privacy_visibility = fields.Selection([
        ('portal', 'Portal'),
        ('public', 'Public'),
        ('private', 'Private'),
        ('followers', 'Followers')
    ], string='Visibility', default='portal', required=True)

    collaborator_count = fields.Integer(compute='_compute_collaborator_count', string='Collaborators')
    task_id = fields.One2many('projects.task', 'project_id', string="Tasks")
    task_count = fields.Integer(compute='_compute_task_count', string='Task Count', store=True)

    @api.depends('task_id')
    def _compute_task_count(self):
        for project in self:
            project.task_count = len(project.task_id)

    def _compute_collaborator_count(self):
        for record in self:
            record.collaborator_count = len(record.message_partner_ids)

    @api.model
    def create(self, vals):
        if vals.get('name'):
            vals['name'] = vals['name'].strip()
        return super(Project, self).create(vals)

    def write(self, vals):
        if vals.get('name'):
            vals['name'] = vals['name'].strip()
        return super(Project, self).write(vals)