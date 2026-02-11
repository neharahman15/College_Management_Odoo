from odoo import api,fields,models
from datetime import date

class CollegeStudents(models.Model):

    _name='college.students'
    _description='College Students'
    _order = 'id desc'
    _inherits = {'res.partner': 'partner_id'}
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name="name"
   
    partner_id=fields.Many2one('res.partner',string='Student Name',ondelete="cascade", required=True)
    # name=fields.Char(string="Student Name",on_delete='cascade')
    mail = fields.Char(string="Email")
    # mail=fields.Char(related='res.partner.email')
    mobile = fields.Char(string="Mobile Number")
    street=fields.Char(string="Street")
    city=fields.Char(string="city")
    state=fields.Many2one('res.country.state')
    zip=fields.Char()
    country=fields.Many2one('res.country')

    dob = fields.Date(string="Date of Birth")

    age=fields.Integer(compute="_compute_age",store=True,tracking=True)

    reference_number=fields.Char(string="Sequence",copy=False,default="New",readonly=True)


    @api.depends('dob')

    def _compute_age(self):

        """compute the age from dob"""
        
        today = date.today()
        for record in self:
            if record.dob:
                record.age = today.year - record.dob.year
                if (today.month, today.day) < (record.dob.month, record.dob.day):
                    record.age -= 1
            else:
                record.age = 0
    

    @api.model_create_multi

    def create(self,vals):

        for rec in vals:

            if rec.get("reference_number","New")=="New":

                code=self.env['ir.sequence'].next_by_code('student.data')
                rec['reference_number']=code

        res = super().create(vals)
        return res

    @api.model
    def name_search(self, name='', domain=None, operator='ilike', limit=100):
        domain = list(domain or [])

        if not name:
            return super().name_search(name,domain,operator,limit)
        
        if name:
            search_domain = ['|', '|', '|',
                ('name', operator, name),
                ('email', operator, name),
                ('mobile', operator, name),
                ('reference_number',operator,name),
            ]
            domain = domain + search_domain

        students = self.search_fetch(domain, limit=limit)
        return [(s.id, s.name) for s in students]

    
    # @api.model
    # def name_search(self, name='', domain=None, operator='ilike', limit=100):
    #    domain = list(domain or [])
    #    if not name:
    #        return super().name_search(name, domain,operator,limit)
    #    domain = ['|', '|',
    #              ('name', operator, name),
    #              ('email', operator, name),
    #              ('mobile', operator, name)]
    #    if domain:
    #        domain = ['&'] + domain
    #    students = self.search_fetch(domain, ['name'], limit=limit)
    #    return [(student.id, student.name) for student in studentss]
       
   
        
