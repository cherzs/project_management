from odoo import models, fields, api, _

class Project(models.Model):
    _name = 'project.management'
    _description = 'Project Management'


    name = fields.Char(string='Project Name', required=True)
    description = fields.Text(string='Description')
    start_date = fields.Date(string='Start Date')
    end_date =fields.Date(string='Ebd Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')],
        string='Status', default='draft')
    