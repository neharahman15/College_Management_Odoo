from odoo import fields,models,api
from datetime import date
from odoo.exceptions import ValidationError


class CollegeSemesterLines(models.Model):
    _name="college.semesterlines"
    _description="college Semester"

    
    product_template_id = fields.Many2one(
        'product.template',
    )
    semester_number=fields.Integer(string ="Number")
    semester_start_date=fields.Date(string="Start Date")
    semester_end_date=fields.Date(string="End Date")
    duration=fields.Integer(string="Months")
    semester_fee=fields.Integer(string="Fee")
    due_date=fields.Date(string="Due Date")
    fee_status=fields.Selection([
        ('not_started','Not Started'),
        ('pending','Pending'),
        ('paid','Paid')
    ],string="Status",default='not_started')

    admission_id=fields.Many2one(
        'college.student.admission',
        ondelete='cascade'
    )
    


   
    