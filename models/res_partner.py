from odoo import fields, models
class ResPartner(models.Model):
    _inherit = 'res.partner'
    is_student = fields.Boolean(string='Is Student', default=False, copy=False)
    student_record_ids = fields.One2many(
        'student.student',
        'partner_id',
        string='Student Records',
    )

