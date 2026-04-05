from odoo import api, fields, models


class StudentAttendance(models.Model):
    _name = 'student.attendance'
    _description = 'Student Attendance'

    name = fields.Char(string='Attendance Reference', required=True, default='New')
    date = fields.Date(string='Date', default=fields.Date.context_today, required=True)
    classroom_id = fields.Many2one('student.classroom', string='Classroom')
    teacher_id = fields.Many2one(
        'res.partner',
        string='Marked By',
        domain=[('is_student', '=', False)],
    )
    line_ids = fields.One2many('student.attendance.line', 'attendance_id', string='Attendance Lines')
    present_count = fields.Integer(string='Present Count', compute='_compute_counts')
    absent_count = fields.Integer(string='Absent Count', compute='_compute_counts')

    @api.depends('line_ids.present')
    def _compute_counts(self):
        for rec in self:
            rec.present_count = sum(1 for line in rec.line_ids if line.present)
            rec.absent_count = len(rec.line_ids) - rec.present_count

    @api.onchange('classroom_id')
    def _onchange_classroom_id(self):
        if self.classroom_id:
            lines = []
            for student in self.classroom_id.student_ids:
                lines.append((0, 0, {'student_id': student.id, 'present': False}))
            self.line_ids = lines


class StudentAttendanceLine(models.Model):
    _name = 'student.attendance.line'
    _description = 'Student Attendance Line'

    attendance_id = fields.Many2one('student.attendance', string='Attendance', required=True, ondelete='cascade')
    student_id = fields.Many2one(
        'res.partner',
        string='Student',
        required=True,
        domain=[('is_student', '=', True)],
    )
    present = fields.Boolean(string='Present', default=False)
    remarks = fields.Text(string='Remarks')
