from odoo import api, fields, models


class StudentAttendance(models.Model):
    _name = 'student.attendance'
    _description = 'Student Attendance'

    name = fields.Char(string='Attendance Reference', required=True, default='New')
    date = fields.Datetime(string='Date & Time', default=fields.Datetime.now, required=True)
    classroom_id = fields.Many2one('student.classroom', string='Batch')
    room_number = fields.Char(string='Room Number')
    department_id = fields.Many2one('student.course', string='Department', required=True)
    subject_id = fields.Many2one(
        'student.subject',
        string='Course',
        required=True,
    )
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

    @api.onchange('department_id', 'subject_id', 'classroom_id')
    def _onchange_subject_or_classroom(self):
        for rec in self:
            rec.line_ids = [(5, 0, 0)]
            if not rec.department_id or not rec.subject_id:
                continue

            domain = [
                ('is_student', '=', True),
                ('course_ids', 'in', rec.department_id.id),
                ('subject_ids', 'in', rec.subject_id.id),
            ]
            if rec.classroom_id:
                domain.append(('classroom_id', '=', rec.classroom_id.id))

            students = self.env['res.partner'].search(domain, order='name asc')
            rec.line_ids = [
                (0, 0, {'student_id': student.id, 'present': False})
                for student in students
            ]


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
