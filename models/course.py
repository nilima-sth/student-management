from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Course(models.Model):
    _name = 'student.course'
    _description = 'Student Department'

    name = fields.Char(string='Department Name', required=True)
    code = fields.Char(string='Department Code')
    program = fields.Selection(
        [
            ('bim', 'BIM'),
            ('csit', 'CSIT'),
        ],
        string='Program',
        default='csit',
        required=True,
    )
    description = fields.Text(string='Description')
    semesters_count = fields.Integer(string='Number of Semester', default=8)
    fee_per_semester = fields.Float(string='Fees per semester')
    subject_ids = fields.Many2many(
        'student.subject',
        'student_subject_department_rel',
        'course_id',
        'subject_id',
        string='Courses'
    )
    sem1_subject_ids = fields.Many2many('student.subject', compute='_compute_semester_subjects', string='Semester 1 Courses')
    sem2_subject_ids = fields.Many2many('student.subject', compute='_compute_semester_subjects', string='Semester 2 Courses')
    sem3_subject_ids = fields.Many2many('student.subject', compute='_compute_semester_subjects', string='Semester 3 Courses')
    sem4_subject_ids = fields.Many2many('student.subject', compute='_compute_semester_subjects', string='Semester 4 Courses')
    sem5_subject_ids = fields.Many2many('student.subject', compute='_compute_semester_subjects', string='Semester 5 Courses')
    sem6_subject_ids = fields.Many2many('student.subject', compute='_compute_semester_subjects', string='Semester 6 Courses')
    sem7_subject_ids = fields.Many2many('student.subject', compute='_compute_semester_subjects', string='Semester 7 Courses')
    sem8_subject_ids = fields.Many2many('student.subject', compute='_compute_semester_subjects', string='Semester 8 Courses')
    student_ids = fields.Many2many(
        'res.partner',
        'student_course_rel',
        'course_id',
        'student_id',
        string='Enrolled Students',
        domain=[('is_student', '=', True)]
    )

    @api.depends('subject_ids', 'subject_ids.semester')
    def _compute_semester_subjects(self):
        for rec in self:
            rec.sem1_subject_ids = rec.subject_ids.filtered(lambda s: s.semester == '1')
            rec.sem2_subject_ids = rec.subject_ids.filtered(lambda s: s.semester == '2')
            rec.sem3_subject_ids = rec.subject_ids.filtered(lambda s: s.semester == '3')
            rec.sem4_subject_ids = rec.subject_ids.filtered(lambda s: s.semester == '4')
            rec.sem5_subject_ids = rec.subject_ids.filtered(lambda s: s.semester == '5')
            rec.sem6_subject_ids = rec.subject_ids.filtered(lambda s: s.semester == '6')
            rec.sem7_subject_ids = rec.subject_ids.filtered(lambda s: s.semester == '7')
            rec.sem8_subject_ids = rec.subject_ids.filtered(lambda s: s.semester == '8')

    @api.constrains('semesters_count')
    def _check_semesters_count(self):
        for rec in self:
            if rec.semesters_count < 1 or rec.semesters_count > 8:
                raise ValidationError('Number of Semester must be between 1 and 8.')

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        self._sync_batch_course_menus()
        return records

    def write(self, vals):
        result = super().write(vals)
        if any(key in vals for key in ['name', 'semesters_count']):
            self._sync_batch_course_menus()
        return result

    def unlink(self):
        result = super().unlink()
        self._sync_batch_course_menus()
        return result

    @api.model
    def _sync_batch_course_menus(self):
        root_menu = self.env.ref('student_management.menu_student_batch', raise_if_not_found=False)
        kanban_view = self.env.ref('student_management.view_student_classroom_kanban', raise_if_not_found=False)
        search_view = self.env.ref('student_management.view_student_classroom_search', raise_if_not_found=False)
        if not root_menu:
            return

        imd_model = self.env['ir.model.data'].sudo()
        menu_model = self.env['ir.ui.menu'].sudo()
        action_model = self.env['ir.actions.act_window'].sudo()

        generated_imd = imd_model.search([
            ('module', '=', 'student_management'),
            ('name', 'like', 'batch_dynamic_%'),
        ])
        for imd in generated_imd:
            if imd.model in ('ir.ui.menu', 'ir.actions.act_window') and imd.res_id:
                rec = self.env[imd.model].sudo().browse(imd.res_id)
                if rec.exists():
                    rec.unlink()
        generated_imd.unlink()

        courses = self.sudo().search([], order='name asc')
        for idx, course in enumerate(courses, start=10):
            course_menu = menu_model.create({
                'name': course.name,
                'parent_id': root_menu.id,
                'sequence': idx,
            })
            imd_model.create({
                'module': 'student_management',
                'name': f'batch_dynamic_course_menu_{course.id}',
                'model': 'ir.ui.menu',
                'res_id': course_menu.id,
                'noupdate': True,
            })

            for sem in range(1, course.semesters_count + 1):
                sem_str = str(sem)
                action = action_model.create({
                    'name': f'{course.name} - Semester {sem_str}',
                    'res_model': 'student.classroom',
                    'view_mode': 'kanban,form',
                    'view_id': kanban_view.id if kanban_view else False,
                    'search_view_id': search_view.id if search_view else False,
                    'domain': f"[('course_id', '=', {course.id}), ('semester', '=', '{sem_str}')]",
                    'context': f"{{'default_course_id': {course.id}, 'default_semester': '{sem_str}'}}",
                })
                imd_model.create({
                    'module': 'student_management',
                    'name': f'batch_dynamic_course_sem_action_{course.id}_{sem_str}',
                    'model': 'ir.actions.act_window',
                    'res_id': action.id,
                    'noupdate': True,
                })

                sem_menu = menu_model.create({
                    'name': f'Semester {sem_str}',
                    'parent_id': course_menu.id,
                    'sequence': sem,
                    'action': f'ir.actions.act_window,{action.id}',
                })
                imd_model.create({
                    'module': 'student_management',
                    'name': f'batch_dynamic_course_sem_menu_{course.id}_{sem_str}',
                    'model': 'ir.ui.menu',
                    'res_id': sem_menu.id,
                    'noupdate': True,
                })
