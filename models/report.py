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


class StudentReportLine(models.Model):
    _name = 'student.report.line'
    _description = 'Student Report Line'

    report_id = fields.Many2one('student.report', string='Report', required=True)
    course_id = fields.Many2one('student.course', string='Course', required=True)
    full_marks = fields.Float(string='Full Marks', required=True, default=100.0)
    pass_marks = fields.Float(string='Pass Marks', required=True, default=40.0)
    obtained_marks = fields.Float(string='Obtained Marks', required=True, default=0.0)
    result=fields.Boolean(string='Result',compute='compute_if_pass')

    @api.depends('obtained_marks', 'pass_marks')
    def compute_if_pass(self):
        for line in self:
            line.result=line.obtained_marks >= line.pass_marks

