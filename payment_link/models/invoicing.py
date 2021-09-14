from odoo import api, fields, models
import hashlib
import hmac


class Invoicing(models.Model):
    _inherit = "account.move"
    link = fields.Char(string='Payment Link')
    access_token = fields.Char()

    def get_link(self):
        secret = self.env['ir.config_parameter'].sudo().\
            get_param('database.secret')
        for rec in self:
            token_str = '%s%s%s' % (rec.partner_id.id,
                                    rec.amount_residual,
                                    rec.currency_id.id)
            rec.access_token = hmac.new(secret.encode('utf-8'),
                                        token_str.encode('utf-8'),
                                        hashlib.sha256).hexdigest()

            self.link = ('%s/website_payment/pay?reference=%s&'
                         'amount=%s&currency_id=%s&'
                         'partner_id=%s&access_token=%s') % (
                   rec.get_base_url(),
                   rec.name,
                   rec.amount_residual,
                   rec.currency_id.id,
                   rec.partner_id.id,
                   rec.access_token
               )

    def action_post(self):
        super(Invoicing, self).action_post()
        self.get_link()
        mail_template = self.env.\
            ref('paymentlink.mail_template_data_payment_link')
        mail_template.send_mail(self.id, force_send=True)
