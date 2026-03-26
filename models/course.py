from odoo import models, fields


class Course(models.Model):
    _name = 'student.course'
    _description = 'Student Course'

    name = fields.Char(string='Course Name', required=True)
    code = fields.Char(string='Course Code')
    description = fields.Text(string='Description')
    duration_months = fields.Integer(string='Duration (Months)')
    fee = fields.Float(string='Course Fee')
    active = fields.Boolean(default=True)
