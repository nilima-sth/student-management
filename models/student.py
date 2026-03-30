from odoo import api, fields, models
class Student(models.Model):
    _inherit = 'res.partner'
    _description = 'Student Record'

    date_of_birth = fields.Date(string='Date of Birth')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    enrollment_date = fields.Date(string='Enrollment Date')
    course_ids = fields.Many2many(
        'student.course',
        'student_course_rel',
        'student_id',
        'course_id',
        string='Courses'
    )

    student_state = fields.Selection([
        ('draft', 'Draft'),
        ('documents_pending', 'Documents Pending'),
        ('approved', 'Approved'),
        ('admitted', 'Admitted'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('not_completed', 'Not Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Student Stage', default='draft')

    def action_admit(self):
        self.write({'student_state': 'admitted'})

    def action_mark_completed(self):
        self.write({'student_state': 'completed'})

    def action_mark_not_completed(self):
        self.write({'student_state': 'not_completed'})

    def action_cancel_student(self):
        self.write({'student_state': 'cancelled'})

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('is_student'):
                vals['is_student'] = True
            if not vals.get('company_type'):
                vals['company_type'] = 'person'
        return super().create(vals_list)

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = fields.Date.today()
        for student in self:
            if student.date_of_birth:
                birthday_passed = (today.month, today.day) >= (
                    student.date_of_birth.month,
                    student.date_of_birth.day,
                )
                student.age = today.year - student.date_of_birth.year
                if not birthday_passed:
                    student.age -= 1
            else:
                student.age = 0
