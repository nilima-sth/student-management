from odoo import api, fields, models
from odoo.exceptions import ValidationError


class StudentClassroom(models.Model):
    _name = 'student.classroom'
    _description = 'Student Batch'

    name = fields.Char(string='Batch Name', required=True)
    year = fields.Char(string='Year', required=True, default=lambda self: str(fields.Date.today().year))
    program = fields.Selection(
        [
            ('bim', 'BIM'),
            ('csit', 'CSIT'),
        ],
        string='Program',
        default='csit',
    )
    semester = fields.Selection(
        [
            ('1', 'Semester 1'),
            ('2', 'Semester 2'),
            ('3', 'Semester 3'),
            ('4', 'Semester 4'),
            ('5', 'Semester 5'),
            ('6', 'Semester 6'),
            ('7', 'Semester 7'),
            ('8', 'Semester 8'),
        ],
        string='Semester',
        default='1',
        required=True,
    )
    class_teacher = fields.Many2one('res.partner', string='Class Teacher', domain=[('is_student', '=', False)])
    course_id = fields.Many2one('student.course', string='Department')
    subject_ids = fields.Many2many(
        'student.subject',
        'classroom_subject_rel',
        'classroom_id',
        'subject_id',
        string='Courses',
    )
    student_ids = fields.One2many('res.partner', 'classroom_id', string='Students')
    student_count = fields.Integer(string='Student Count', compute='_compute_student_count')

    @api.depends('student_ids')
    def _compute_student_count(self):
        for rec in self:
            rec.student_count = len(rec.student_ids)

    @api.onchange('course_id')
    def _onchange_course_id(self):
        for rec in self:
            if rec.course_id and rec.semester and int(rec.semester) > rec.course_id.semesters_count:
                rec.semester = str(rec.course_id.semesters_count)
            if rec.course_id and rec.program != rec.course_id.program:
                rec.program = rec.course_id.program
            rec.subject_ids = [(5, 0, 0)]

    @api.constrains('course_id', 'semester')
    def _check_semester_in_course_limit(self):
        for rec in self:
            if rec.course_id and rec.semester and int(rec.semester) > rec.course_id.semesters_count:
                raise ValidationError('Semester must be within the course Number of Semester.')
