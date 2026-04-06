from odoo import api, fields, models


class StudentClassroomRoom(models.Model):
    _name = 'student.classroom.room'
    _description = 'Student Classroom'

    name = fields.Char(string='Classroom Name', compute='_compute_name', store=True)
    room_number = fields.Char(string='Room Number', required=True)
    batch_id = fields.Many2one('student.classroom', string='Batch', required=True)
    department_id = fields.Many2one('student.course', string='Department', required=True)
    course_id = fields.Many2one('student.subject', string='Course', required=True)

    @api.depends('room_number', 'batch_id')
    def _compute_name(self):
        for rec in self:
            if rec.batch_id:
                rec.name = f"Room {rec.room_number} - {rec.batch_id.name}"
            else:
                rec.name = f"Room {rec.room_number}"

    @api.onchange('batch_id')
    def _onchange_batch_id(self):
        for rec in self:
            if rec.batch_id and rec.department_id != rec.batch_id.course_id:
                rec.department_id = rec.batch_id.course_id
                rec.course_id = False
