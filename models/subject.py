from odoo import fields, models


class StudentSubject(models.Model):
    _name = 'student.subject'
    _description = 'Student Subject'

    name = fields.Char(string='Subject Name', required=True)
    code = fields.Char(string='Subject Code')
    course_id = fields.Many2one('student.course', string='Course')
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
    description = fields.Text(string='Description')
