from odoo import models, fields

class Task(models.Model):
    _name = 'projects.task'
    _description = 'Project Task'

    # Fields for task
    name = fields.Char(string='Task Name', required=True)
    project_id = fields.Many2one('project.management', string='Project', ondelete='cascade')
    assigned_user_id = fields.Many2one('res.users', string='Assigned To')
    description = fields.Text(string='Description')
    date_deadline = fields.Date(string='Deadline')
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')],
        string='Status', default='new')
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
        ('2', 'High')],
        string='Priority', default='1')
    project_id = fields.Many2one('project.management', string='Project')

    tag_ids = fields.Many2many('project.tags', string='Tags')