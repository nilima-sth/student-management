from odoo import api, fields, models


class Student(models.Model):
    _inherit = 'res.partner'
    _description = 'Student Record'

    date_of_birth = fields.Date(string='Date of Birth')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    enrollment_date = fields.Date(string='Enrollment Date', default=fields.Date.today)
    course_ids = fields.Many2many(
        'student.course',
        'student_course_rel',
        'student_id',
        'course_id',
        string='Courses'
    )
    guardian_ids = fields.One2many('student.guardian', 'student_id', string='Guardians')

    student_state = fields.Selection([
        ('draft', 'Draft'),
        ('documents_pending', 'Documents Pending'),
        ('approved', 'Approved'),
        ('admitted', 'Admitted'),
        ('active', 'Active'),
        ('alumni', 'Alumni'),
        ('cancelled', 'Cancelled'),
    ], string='Student Stage', default='draft')

    def action_admit(self):
        self.write({'student_state': 'admitted'})

    def action_alumni(self):
        self.write({'student_state': 'alumni'})

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
                if student.age < 0:
                    student.age = 0
            else:
                student.age = 0

    @api.onchange('date_of_birth')
    def _onchange_date_of_birth_warning(self):
        today = fields.Date.today()
        if self.date_of_birth and self.date_of_birth > today:
            self.age = 0
            return {
                'warning': {
                    'title': 'Warning',
                    'message': 'Future date of birth is not allowed. Age has been set to 0.',
                }
            }

