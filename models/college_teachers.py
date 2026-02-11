from odoo import api,fields,models
from datetime import date

class CollegeTeachers(models.Model):
    """teacher model-basic fields+ many2one(course)"""

    _name='college.teachers' 
    _description='College Teachers'   
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name=fields.Char(string="Teacher Name")
    email=fields.Char(string="Email")
    mobile=fields.Char()
    department=fields.Char()
    
    reference_num=fields.Char(string="sequence",copy=False,default="New",readonly=True)


    @api.model_create_multi

    def create(self,vals):
        """sequence number generation"""
        for rec in vals:
            if rec.get("reference_num","New")=="New":
                code=self.env['ir.sequence'].next_by_code('teacher.data')
                rec['reference_num']=code
        res = super().create(vals)
        return res
    