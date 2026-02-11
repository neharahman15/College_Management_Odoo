from odoo import models, fields, api
from datetime import timedelta

class ProductTemplate(models.Model):

    _inherit = 'product.template'

    is_course = fields.Boolean(string="Is Course")
    total_semester = fields.Integer(string="Total Semester")
    start_date = fields.Date()
    
    semester_ids = fields.One2many(
        'college.semesterlines',
        'product_template_id',
        string="Semesters",
    )

    show_semester_id=fields.Boolean(default=False)
 
    def generate_semester_plan(self):

        for rec in self:

            semester_start_date=rec.start_date
            semester_end_date = rec.start_date + timedelta(days=180)
            sem_fee=rec.list_price/rec.total_semester

            semester_lines=[]

            for i in range(1, rec.total_semester + 1):
                # self.env['product.template'].write({
                #     'semester_id':
               semester_lines.append(
                    (0, 0, {
                                'product_template_id': self.id,
                                'semester_number': i,
                                'semester_start_date': semester_start_date,
                                'semester_end_date': semester_end_date,
                                'duration': 6,
                                'semester_fee': sem_fee,
                            })
               )
               semester_start_date=semester_end_date + timedelta(days=1)
               semester_end_date=semester_start_date+timedelta(days=180)

            rec.semester_ids=semester_lines
            rec.show_semester_id=True

    def clear_semester_plan(self):

        for rec in self:
            rec.update({
                'semester_ids': [(5, 0, 0)],
                'show_semester_id': False
                })


    @api.onchange('is_course')

    def _onchange_is_course(self):

        if self.is_course:
            self.type = 'service'
    
   