from odoo import fields, models
class StudentGuardian(models.Model):
    _name = 'student.guardian'
    _description = 'Student Guardian'

    name = fields.Char(string='Guardian Name', required=True)
    student_id = fields.Many2one(
        'res.partner',
        string='Student',
        required=True, #You cannot create a guardian without selecting a student.
        ondelete='cascade', #If the student is deleted → automatically delete the guardian.
        domain=[('is_student', '=', True)], #This is a filter
    )
    relationship = fields.Selection(  
        [
            ('father', 'Father'),
            ('mother', 'Mother'),
            ('brother', 'Brother'),
            ('sister', 'Sister'),
            ('guardian', 'Guardian'),
            ('other', 'Other'),
        ],
        string='Relationship',
        required=True,
    )
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    address = fields.Text(string='Address')