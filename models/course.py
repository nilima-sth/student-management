from odoo import models, fields


class Course(models.Model):
    _name = 'student.course'
    _description = 'Student Course'

    name = fields.Char(string='Course Name', required=True)
    code = fields.Char(string='Course Code')
    program = fields.Selection(
        [
            ('bim', 'BIM'),
            ('csit', 'CSIT'),
        ],
        string='Course',
        default='csit',
        required=True,
    )
    description = fields.Text(string='Description')
    semesters_count = fields.Integer(string='Number of Semester', default=8)
    fee_per_semester = fields.Float(string='Fees per semester')
    subject_ids = fields.One2many('student.subject', 'course_id', string='Subjects')
    student_ids = fields.Many2many(
        'res.partner',
        'student_course_rel',
        'course_id',
        'student_id',
        string='Enrolled Students',
        domain=[('is_student', '=', True)]
    )
