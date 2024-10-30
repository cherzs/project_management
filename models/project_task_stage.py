from odoo import models, fields, api

class ProjectTaskStage(models.Model):
    _name = 'project.task.stage.personal'
    _description = 'Personal Task Stage'
    _order = 'sequence, id'

    name = fields.Char(string='Stage Name', required=True, translate=True)
    sequence = fields.Integer(string='Sequence', default=10)
    user_id = fields.Many2one('res.users', string='User', required=True, default=lambda self: self.env.user)
    fold = fields.Boolean(string='Folded in Kanban')
    active = fields.Boolean(default=True) 