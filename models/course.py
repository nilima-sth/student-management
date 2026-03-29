from odoo import models, fields


class Course(models.Model):
    _name = 'student.course'
    _description = 'Student Course'

    name = fields.Char(string='Course Name', required=True)
    code = fields.Char(string='Course Code')
    description = fields.Text(string='Description')
    duration_months = fields.Integer(string='Duration (Months)')
    fee = fields.Float(string='Course Fee')
    student_ids = fields.Many2many(
        'res.partner',
        'student_course_rel',
        'course_id',
        'student_id',
        string='Enrolled Students',
        domain=[('is_student', '=', True)]
    )
