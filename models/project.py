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
    
    sequence = fields.Integer("Sequence", default=10)
    color = fields.Integer("Color") 
    active = fields.Boolean(string='Active', default=True)
    partner_id = fields.Many2one('res.partner', string='Customer')
    
    # Project management specific fields
    tag_ids = fields.Many2many('project.tags', string='Tags')
    
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
