from odoo import models, fields

class Project(models.Model):
    _name = 'project.management'
    _description = 'Project Management'

    # Core fields
    name = fields.Char(string='Project Name', required=True)
    user_id = fields.Many2one('res.users', string='Assigned User')
    date = fields.Datetime(string='Date')
    description = fields.Text(string='Description')
    date_start = fields.Datetime(string="Start Date")
    date_end = fields.Datetime(string="End Date")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')],
        string='Status', default='draft')

    # Additional fields for the project structure
    subtask_ids = fields.One2many(
        'project.management', 'parent_id', string='Sub-tasks'
    )
    parent_id = fields.Many2one('project.management', string='Parent Task')
    recurrence_id = fields.Many2one('recurrence.model', string='Recurrence')
    
    # Project settings and features
    allow_task_dependencies = fields.Boolean(string='Allow Task Dependencies')
    rating_last_value = fields.Float(string='Last Rating Value')
    rating_count = fields.Integer(string='Rating Count', default=0)
    allow_milestones = fields.Boolean(string='Allow Milestones')
    company_id = fields.Many2one('res.company', string='Company')
    project_id = fields.Many2one('project.project', string='Project')
    stage_id = fields.Many2one('project.task.type', string='Stage')
    personal_stage_type_id = fields.Many2one('project.stage.type', string='Personal Stage')
    sequence = fields.Integer("Sequence", default=10)
    color = fields.Integer("Color") 
    active = fields.Boolean(string='Active', default=True)
    partner_id = fields.Many2one('res.partner', string='Customer')
    
    # Project management specific fields
    tag_ids = fields.Many2many('project.tags', string='Tags')
    last_update_status = fields.Char(string='Last Update Status')
    last_update_color = fields.Char(string='Last Update Color')
    
    # Fields for the form view's header and buttons
    privacy_visibility = fields.Selection([
        ('portal', 'Portal'),
        ('public', 'Public'),
        ('private', 'Private'),
        ('followers', 'Followers')
    ], string='Visibility', default='portal')

    # Field for tracking collaborators count
    collaborator_count = fields.Integer(compute='_compute_collaborator_count', string='Collaborators')

    def _compute_collaborator_count(self):
        for record in self:
            # Logic to compute the number of collaborators for the project
            record.collaborator_count = 0  # Replace with actual logic
