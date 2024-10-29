from odoo import models, fields, api
from datetime import timedelta

class Task(models.Model):
    _name = 'projects.task'
    _description = 'Project Task'
    
    name = fields.Char(string='Task Name', required=True, tracking=True)
    project_id = fields.Many2one('project.management', string='Project', required=True, tracking=True)
    assigned_user_id = fields.Many2one('res.users', string='Assigned To', tracking=True)
    description = fields.Text(string='Description', tracking=True)
    date_deadline = fields.Date(string='Deadline', tracking=True)
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='new', tracking=True)
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
        ('2', 'High')
    ], string='Priority', default='1', tracking=True)
    color = fields.Integer(string='Color Index')
    tag_ids = fields.Many2many('project.tags', string='Tags')
    
    time_group = fields.Selection([
        ('overdue', 'Overdue'),
        ('today', 'Today'),
        ('this_week', 'This Week'),
        ('next_week', 'Next Week'),
        ('later', 'Later'),
        ('done', 'Done')
    ], string='Time Group', compute='_compute_time_group', store=True)

    @api.depends('date_deadline', 'state')
    def _compute_time_group(self):
        today = fields.Date.today()
        for task in self:
            if task.state == 'done':
                task.time_group = 'done'
            elif not task.date_deadline:
                task.time_group = 'later'
            elif task.date_deadline < today:
                task.time_group = 'overdue'
            elif task.date_deadline == today:
                task.time_group = 'today'
            elif task.date_deadline <= today + timedelta(days=7):
                task.time_group = 'this_week'
            elif task.date_deadline <= today + timedelta(days=14):
                task.time_group = 'next_week'
            else:
                task.time_group = 'later'
