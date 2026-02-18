from odoo import models, fields

class AccountMove(models.Model):
    _inherit='account.move'

#invoice in student admission
    admission_id=fields.Many2one('college.student.admission')

