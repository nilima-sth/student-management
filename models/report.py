from odoo import fields, models, api

class StudentReport(models.Model):
    _name = 'student.report'
    _description = 'Student Report'

    name = fields.Char(string='Report Reference', required=True)
    exam_type = fields.Selection([
        ('mid_term', 'Mid-Term'),
        ('pre_board', 'Pre-board'),
    ], string='Exam Type', default='mid_term', required=True)
    student_id = fields.Many2one('res.partner', string='Student', required=True, domain=[('is_student', '=', True)])
    student_roll_no = fields.Char(related='student_id.roll_no', string='Roll Number', readonly=True)
    student_batch_id = fields.Many2one(related='student_id.classroom_id', string='Batch', readonly=True)
    student_department_ids = fields.Many2many(related='student_id.course_ids', string='Department', readonly=True)
    report_date = fields.Date(string='Report Date', default=fields.Date.context_today, required=True)
    line_ids = fields.One2many('student.report.line', 'report_id', string='Report Lines')
    remarks = fields.Text(string='Remarks')
    state = fields.Selection([
        ('1', 'Draft'),
        ('2', 'Confirmed')
    ], string='Status', default='1')
    total_obtained = fields.Float(string='Total Obtained', compute='_compute_total_obtained')

    @api.depends('line_ids.obtained_marks')
    def _compute_total_obtained(self):
        for rec in self:
            total = 0.0
            for line in rec.line_ids:
                try:
                    total += float(line.obtained_marks or 0.0)
                except Exception:
                    total += 0.0
            rec.total_obtained = total

    @api.onchange('student_id')
    def _onchange_student_id_populate_lines(self):
        for rec in self:
            if not rec.student_id:
                rec.line_ids = [(5, 0, 0)]
                continue
            subjects = rec._get_student_subjects()
            line_vals = []
            for subject in subjects:
                line_vals.append((0, 0, {
                    'course_id': subject.id,
                }))
            rec.line_ids = line_vals

    def _get_student_subjects(self):
        self.ensure_one()
        student = self.student_id
        if not student:
            return self.env['student.subject']
        if student.classroom_id and student.classroom_id.subject_ids:
            return student.classroom_id.subject_ids
        if student.subject_ids:
            return student.subject_ids
        if student.classroom_id and student.classroom_id.course_id:
            subjects = student.classroom_id.course_id.subject_ids
            if student.classroom_id.semester:
                subjects = subjects.filtered(lambda s: s.semester == student.classroom_id.semester)
            return subjects
        return self.env['student.subject']


class StudentReportLine(models.Model):
    _name = 'student.report.line'
    _description = 'Student Report Line'

    report_id = fields.Many2one('student.report', string='Report', required=True)
    course_id = fields.Many2one('student.subject', string='Course', required=True)
    full_marks = fields.Float(string='Full Marks', required=True, default=100.0)
    pass_marks = fields.Float(string='Pass Marks', required=True, default=40.0)
    obtained_marks = fields.Float(string='Obtained Marks', required=True, default=0.0)
    result=fields.Boolean(string='Result',compute='compute_if_pass')

    @api.depends('obtained_marks', 'pass_marks')
    def compute_if_pass(self):
        for line in self:
            line.result=line.obtained_marks >= line.pass_marks
