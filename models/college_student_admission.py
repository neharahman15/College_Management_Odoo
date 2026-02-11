from odoo import api,fields,models
from datetime import date
from datetime import timedelta
from odoo.exceptions import ValidationError


class CollegeStudentAdmission(models.Model):
    _name='college.student.admission'
    _description='College_Student_Admission'
    _order ='id desc'
    _inherit = ['mail.thread']
    _rec_name="name"

    Admission_Number=fields.Char(string="Admission No", default="New",copy=False,readonly=True)

    name=fields.Many2one('college.students' ,required=True)

    responsible=fields.Many2one('res.users',
                            string='Responsible',
                            readonly=True,
                            default=lambda self: self.env.user)

    course=fields.Many2one('product.template',
                            domain=[('is_course', '=' ,True)],)

    assigned_teacher=fields.Many2one('college.teachers',
                                        string="Teacher",
                                        required=True)

    departmentt=fields.Char(related='assigned_teacher.department')

    total_course_fee=fields.Float(related='course.list_price' ,string='Course fee')

    paid_amount=fields.Float(compute='sum_invoice_amount',string="Amount Paid")

    balance_amount=fields.Float(compute='balance_invoice_amount',string="Amount Balance")

    admission_date=fields.Date(default=date.today())

    status = fields.Selection(selection=[
       ('draft', 'Draft'),
       ('submitted','Submitted'),
       ('approved', 'Approved'),
       ('rejected', 'Rejected'),
       ('invoiced', 'Invoiced'),],
       string='Status', required=True, readonly=True, copy=False,default='draft',tracking=True)

    admission_semesterline_ids=fields.One2many(
        'college.semesterlines',
        'admission_id')

    invoice_count=fields.Integer(compute='_compute_invoice_count')
    invoice_id=fields.One2many('account.move',
                                'admission_id')


    @api.model_create_multi

    def create(self,vals):

        for rec in vals:

            if rec.get("Admission_Number","New")=="New":

                code=self.env['ir.sequence'].next_by_code('admission.number')
                rec["Admission_Number"]=code

        res=super().create(vals)
        return res
    
    # @api.onchange('course')
    # def _onchange_course(self):
    #     if self.course:
    #         self.admission_semesterline_ids=self.course.semester_ids


    @api.onchange('course')

    def _onchange_course(self):

        if self.course:
            
            self.admission_semesterline_ids = [(5, 0, 0)]

            admission_semester_lines=[]

            for i in self.course.semester_ids:

                admission_semester_lines.append((0,0,{
                    'product_template_id': self.course.id,
                    'semester_number': i.semester_number,
                    'semester_start_date':i.semester_start_date,
                    'semester_end_date': i.semester_end_date,
                    'duration': i.duration,
                    'semester_fee':i.semester_fee,
                    'due_date': (i.semester_start_date + timedelta(days=30)),
                    'fee_status':i.fee_status
                          
                }))
            self.admission_semesterline_ids=admission_semester_lines


    def action_submit(self):
        self.status='submitted'

    def action_cancel(self):
        self.status='draft'

    def action_approve(self):
        for rec in self:
            rec.status='approved'
            if rec.admission_semesterline_ids:
                rec.admission_semesterline_ids[0].fee_status='pending'

            student_template = self.env.ref(
                            'college_management.email_template_student_admission',)
                                                         
            if student_template:
                student_template.send_mail(rec.id,force_send=False)

            teacher_template = self.env.ref(
                            'college_management.email_template_teacher_admission')
                                        
            if teacher_template:
                teacher_template.send_mail(rec.id,force_send=False)


    def action_reject(self):
        self.status='rejected'
    
    def action_rejected(self):
        self.status='draft'

    # def action_create_invoice(self):
    #     self.status='invoiced'

    pending_semester=fields.Boolean(compute="_fee_status_is_pending",
                                    string="is_pending")

    @api.depends('admission_semesterline_ids.fee_status')
    def _fee_status_is_pending(self):
        # for rec in self:
        #     rec.pending_semester = False
        #     for i in rec.admission_semesterline_ids:
        #         if i.fee_status=='pending':
        #             rec.pending_semester=True

        for rec in self:
            rec.pending_semester = bool(
                rec.admission_semesterline_ids.filtered(
                    lambda l: l.fee_status == 'pending'
                )
            )

    def action_create_invoice(self):
        self.ensure_one()

        pending_line=self.admission_semesterline_ids.filtered(
            lambda l:l.fee_status == 'pending'
        )
        if not pending_line:
            return

        pending_line.ensure_one()

        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.name.partner_id.id,
            'admission_id': self.id, 
            'invoice_line_ids': [(0, 0, {
                'name':f"{self.course.name}\n{self.Admission_Number}\n Semester {pending_line.semester_number}",
                # 'product_id': self.course.id,
                'product_id':self.course.product_variant_id.id,
                'quantity': 1,
                # 'price_unit': self.course.list_price,
                'price_unit':pending_line.semester_fee
            })]
        })
        self.status = 'invoiced'
    
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
        }

    def action_view_invoice(self):
    
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "domain": [('admission_id', '=', self.id)],
            "context": {"create": False, 'default_move_type': 'out_invoice'},
            "name": "Invoices",
            'view_mode': 'list,form',
        }
        
   
    def _compute_invoice_count(self):
        for rec in self:
            rec.invoice_count = self.env['account.move'].search_count([
            ('admission_id', '=', rec.id),
            ('move_type', '=', 'out_invoice'),
            ('state','in',['draft','posted'])
        ])

    def sum_invoice_amount(self):
        for rec in self:
            sum=0
            for i in rec.invoice_id:
                if i.status_in_payment=='paid':
                    sum+=i.amount_total
            rec.paid_amount=sum

    def balance_invoice_amount(self):
        for rec in self:
            am=rec.total_course_fee-rec.paid_amount
            rec.balance_amount=am
                


           
    
       

            



        


        

            
   

    
    
    



