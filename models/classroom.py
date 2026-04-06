from odoo import api, fields, models


class StudentClassroom(models.Model):
    _name = 'student.classroom'
    _description = 'Student Classroom'

    name = fields.Char(string='Classroom Name', required=True)
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
    class_teacher = fields.Many2one(
        'res.partner',
        string='Class Teacher',
        domain=[('is_student', '=', False)],
    )
    course_id = fields.Many2one('student.course', string='Course')
    subject_ids = fields.Many2many(
        'student.subject',
        'classroom_subject_rel',
        'classroom_id',
        'subject_id',
        string='Subjects',
    )
    student_ids = fields.One2many('res.partner', 'classroom_id', string='Students')
    student_count = fields.Integer(string='Student Count', compute='_compute_student_count')

    @api.depends('student_ids')
    def _compute_student_count(self):
        for rec in self:
            rec.student_count = len(rec.student_ids)
