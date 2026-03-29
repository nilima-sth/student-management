from odoo import api, fields, models
class Student(models.Model):

    _name = 'student.student'
    _description = 'Student Record'

    partner_id = fields.Many2one(
        'res.partner',
        string='Contact',
        readonly=True,
        copy=False,
        ondelete='cascade',
    )
    name = fields.Char(string='Name', required=True)
    image_1920 = fields.Image(string='Photo')
    date_of_birth = fields.Date(string='Date of Birth')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    email = fields.Char(string='Email')
    enrollment_date = fields.Date(string='Enrollment Date')
    course_ids = fields.Many2many(
        'student.course',
        'student_course_rel',
        'student_id',
        'course_id',
        string='Courses'
    )
    is_adult = fields.Boolean(string='Is Adult', compute='_compute_is_adult', store=True)
    
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('documents_pending', 'Documents Pending'),
        ('approved', 'Approved'),
        ('admitted', 'Admitted'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Stage', default='draft')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('partner_id'):
                partner = self.env['res.partner'].browse(vals['partner_id'])
                partner.write(self._prepare_partner_vals(vals))
            else:
                partner = self.env['res.partner'].create(self._prepare_partner_vals(vals))
                vals['partner_id'] = partner.id
        return super().create(vals_list)

    def write(self, vals):
        result = super().write(vals)
        partner_vals = self._prepare_partner_vals(vals)
        if partner_vals:
            for student in self.filtered('partner_id'):
                student.partner_id.write(partner_vals)
        return result

    def unlink(self):
        partners = self.mapped('partner_id')
        result = super().unlink()
        partners.unlink()
        return result

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = fields.Date.today()
        for student in self:
            if student.date_of_birth:
                student.age = today.year - student.date_of_birth.year - (
                    (today.month, today.day) < (student.date_of_birth.month, student.date_of_birth.day)
                )
            else:
                student.age = 0

    @api.depends('age')
    def _compute_is_adult(self):
        for student in self:
            student.is_adult = (student.age or 0) >= 18

    def _prepare_partner_vals(self, vals):
        partner_vals = {'is_student': True}

        if vals.get('name'):
            partner_vals['name'] = vals['name']
        if 'email' in vals:
            partner_vals['email'] = vals['email']
        if 'image_1920' in vals:
            partner_vals['image_1920'] = vals['image_1920']

        partner_vals.setdefault('company_type', 'person')
        return partner_vals
    