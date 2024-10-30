from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Project(models.Model):
    _name = 'project.management'
    _description = 'Project Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'

    name = fields.Char(string='Project Name', required=True, tracking=True, index=True)
    user_id = fields.Many2one('res.users', string='Project Manager', tracking=True, index=True)
    date = fields.Datetime(string='Date', default=fields.Datetime.now)
    description = fields.Text(string='Description')
    date_start = fields.Date(string="Start Date", index=True)
    date_end = fields.Date(string="End Date")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', required=True, tracking=True, index=True)
    
    sequence = fields.Integer("Sequence", default=10)
    color = fields.Integer("Color")
    active = fields.Boolean(string='Active', default=True, index=True)
    partner_id = fields.Many2one('res.partner', string='Customer', index=True)
    is_favorite = fields.Boolean(string='Show Project on dashboard', default=False)
    tag_ids = fields.Many2many('projects.tags', string='Tags')
    
    privacy_visibility = fields.Selection([
        ('portal', 'Portal'),
        ('public', 'Public'),
        ('private', 'Private'),
        ('followers', 'Followers')
    ], string='Visibility', default='portal', required=True)

    collaborator_count = fields.Integer(compute='_compute_collaborator_count', string='Collaborators')
    task_id = fields.One2many('projects.task', 'project_id', string="Tasks")
    task_count = fields.Integer(compute='_compute_task_count', string='Tasks')
    overdue_task_count = fields.Integer(compute='_compute_task_count', string='Overdue Tasks')

    # Add company support
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Project name must be unique!'),
        ('date_check', 'CHECK(date_start <= date_end)', 'End Date must be after Start Date!')
    ]

    def action_view_tasks(self):
        """Open the task view for this project."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Tasks'),
            'res_model': 'projects.task',
            'view_mode': 'kanban,tree,form',
            'domain': [('project_id', '=', self.id)],
            'context': {
                'default_project_id': self.id,
                'search_default_project_id': self.id,
            },
            'target': 'current',
        }

    @api.depends('task_id')
    def _compute_task_count(self):
        """Compute the number of tasks in the project."""
        for project in self:
            project.task_count = len(project.task_id)

    def _compute_collaborator_count(self):
        for record in self:
            record.collaborator_count = len(record.message_partner_ids)

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if record.date_start and record.date_end and record.date_start > record.date_end:
                raise ValidationError(_('End Date cannot be earlier than Start Date!'))

    def action_start_project(self):
        self.ensure_one()
        if not self.date_start:
            self.date_start = fields.Date.today()
        self.write({'state': 'ongoing'})

    def action_complete_project(self):
        self.ensure_one()
        if not self.date_end:
            self.date_end = fields.Date.today()
        self.write({'state': 'completed'})