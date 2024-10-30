from odoo import models, fields

class ProjectTaskStage(models.Model):
    _name = 'project.task.stage'
    _description = 'Task Stage'
    _order = 'sequence, id'

    name = fields.Char(string='Stage Name', required=True, translate=True)
    sequence = fields.Integer(string='Sequence', default=10)
    fold = fields.Boolean(string='Folded in Kanban')
    active = fields.Boolean(default=True)
    project_ids = fields.Many2many('project.management', string='Projects')