from odoo import api, fields, models


class StudentIDCardWizard(models.TransientModel):
    _name = 'student.id.card.wizard'
    _description = 'Student ID Card Wizard'

    student_id = fields.Many2one(
        'res.partner',
        string='Student',
        domain=[('is_student', '=', True)],
        required=True,
    )

    def print_id_card(self):
        self.ensure_one()
        report = self.env.ref('student_management.report_student_id_card_action')
        return report.report_action(self.student_id)
