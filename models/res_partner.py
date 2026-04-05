from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_student = fields.Boolean(string='Is Student', default=False, copy=False)
    classroom_id = fields.Many2one('student.classroom', string='Classroom')
    attendance_present = fields.Boolean(string='Present', default=False)

