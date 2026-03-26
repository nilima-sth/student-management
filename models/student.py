from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Student(models.Model):
    
    _name = 'student.student'
    _description = 'Student Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    image_1920 = fields.Image(string='Photo')
    date_of_birth = fields.Date(string='Date of Birth')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    email = fields.Char(string='Email')
    enrollment_date = fields.Date(string='Enrollment Date')
    course_ids = fields.Many2many(
        'student.course',
        'student_course_rel',
        'student_id',
        'course_id',
        string='Courses'
    )
    is_adult = fields.Boolean(string='Is Adult', compute='_compute_is_adult', store=True)
    
    
    state = fields.Selection([
        ('not_admitted', 'Not Admitted'),
        ('admitted', 'Admitted')
    ], string='Status', default='not_admitted')

    def action_admit(self):
        self.write({'state': 'admitted'})

    def action_set_not_admitted(self):
        self.write({'state': 'not_admitted'})

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = fields.Date.today()
        for student in self:
            if student.date_of_birth:
                student.age = today.year - student.date_of_birth.year - (
                    (today.month, today.day) < (student.date_of_birth.month, student.date_of_birth.day)
                )
            else:
                student.age = 0

    @api.depends('age')
    def _compute_is_adult(self):
        for student in self:
            student.is_adult = (student.age or 0) >= 18

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        today = fields.Date.today()
        for student in self:
            if student.date_of_birth and student.date_of_birth > today:
                raise ValidationError("Date of Birth cannot be in the future.")


