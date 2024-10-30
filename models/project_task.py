from odoo import models, fields, api

class ProjectTask(models.Model):
    _name = 'projects.task'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Project Task'

    name = fields.Char(string='Task Title', required=True, tracking=True)
    description = fields.Html(string='Description')
    project_id = fields.Many2one('project.management', string='Project', required=True)
    assigned_user_id = fields.Many2one('res.users', string='Assigned To', default=lambda self: self.env.user)
    date_deadline = fields.Date(string='Deadline')
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
        ('2', 'High'),
        ('3', 'Urgent')
    ], string='Priority', default='1')
    tag_ids = fields.Many2many('project.tags', string='Tags')
    stage_id = fields.Many2one('project.task.stage', string='Stage', default=lambda self: self.env['project.task.stage'].search([], limit=1))
    
    # Basic tracking fields
    sequence = fields.Integer(string='Sequence', default=10)
    date_assign = fields.Datetime(string='Assigned Date')
    date_last_stage_update = fields.Datetime(string='Last Stage Update')
    ref = fields.Char(string='Reference')
    parent_id = fields.Many2one('projects.task', string='Parent Task')
    child_ids = fields.One2many('projects.task', 'parent_id', string='Subtasks')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    notes = fields.Text(string='Internal Notes')

    # Time tracking fields
    planned_hours = fields.Float(string='Initially Planned Hours', default=0)
    effective_hours = fields.Float(string='Hours Spent', default=0)
    remaining_hours = fields.Float(string='Remaining Hours', compute='_compute_remaining_hours', store=True)
    total_hours_spent = fields.Float(string='Total Hours', compute='_compute_total_hours', store=True)
    progress = fields.Float(string='Progress', compute='_compute_progress', store=True)
    date_start = fields.Datetime(string='Start Date')
    date_end = fields.Datetime(string='End Date')

    @api.depends('planned_hours', 'effective_hours')
    def _compute_remaining_hours(self):
        for task in self:
            task.remaining_hours = task.planned_hours - task.effective_hours

    @api.depends('effective_hours', 'child_ids.effective_hours')
    def _compute_total_hours(self):
        for task in self:
            total = task.effective_hours
            for child in task.child_ids:
                total += child.effective_hours
            task.total_hours_spent = total

    @api.depends('effective_hours', 'planned_hours')
    def _compute_progress(self):
        for task in self:
            if task.planned_hours > 0:
                task.progress = round(100.0 * task.effective_hours / task.planned_hours, 2)
            else:
                task.progress = 0.0

    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        self.date_last_stage_update = fields.Datetime.now()

    @api.onchange('assigned_user_id')
    def _onchange_assigned_user_id(self):
        if self.assigned_user_id:
            self.date_assign = fields.Datetime.now()
