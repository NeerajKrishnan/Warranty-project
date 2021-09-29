import time
from datetime import date, datetime
import pytz
import json
import datetime
import io
from odoo import api, fields, models, _
from odoo.tools import date_utils
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter



class ReportWizard(models.TransientModel):
    _name = 'report.wizard'
    _description = 'Warranty Report'
    partner_id = fields.Many2one("res.partner")
    product_list = fields.Many2many('product.product')
    to_date = fields.Date(string='End date')
    from_date = fields.Date(string='Start date')

    def action_print(self):
        self.ensure_one()
        temp_list = str(self.product_list.mapped('id'))
        temp_list='('+temp_list[1:-1]+")"
        sql = 'select * from warranty_request'
        if self.partner_id:
            sql += " where customer_id="+str(self.partner_id.id)+""
            if self.product_list:
                sql += " and product_id in "+temp_list
            if self.from_date:
                if self.to_date:
                    sql+=" and (requested_date  between '"+str(self.from_date)\
                         +"' and '"+str(self.to_date)+"')"
                else:
                    sql += " and (requested_date between '" + str(self.from_date) \
                           + "' and '" + str(fields.Date.today())+"')"

            print(self.partner_id.read()[0])
            self.env.cr.execute(sql)
            record = self.env.cr.dictfetchall()
            print(record)
            # print(self.product_list.read()[0])

            data = {
                'is_partner':{'is_partner':self.partner_id},
                'partner': self.partner_id.read()[0],
                'field_info': self.read()[0],
                'product_list':self.product_list.read(),
                'data': record
            }

            return self.env.ref('warranty.action_report_warranty_wizzard') \
                .report_action(self, data=data)


        if self.product_list:
            print(self.read()[0])
            sql += " where  product_id in "+temp_list
            if self.from_date:
                if self.to_date:
                    sql+=" and (requested_date between  '"+str(self.from_date)\
                         +"' and '"+str(self.to_date)+"')"
                else:
                    sql += " and (requested_date between '" + str(self.from_date) \
                           + "' and '" + str(fields.Date.today())+"')"
            print(sql)
            self.env.cr.execute(sql)
            record = self.env.cr.dictfetchall()
            print(record)
            print( self.product_list.read())
            data = {
                'is_partner': {'is_partner': self.partner_id},
                'field_info': self.read()[0],
                'product_list': self.product_list.read(),
                'data': record
            }

            return self.env.ref('warranty.action_report_warranty_wizzard') \
                .report_action(self, data=data)


        if self.from_date:
            if self.to_date:
                sql+=" where  (requested_date between '"+str(self.from_date)\
                         +"' and '"+str(self.to_date)+"')"
            else:
                sql += " where (requested_date between '" + str(self.from_date) \
                           + "' and '" + str(fields.Date.today())+"')"

            print(sql)
            self.env.cr.execute(sql)
            record = self.env.cr.dictfetchall()
            print(record)

            data = {
                'is_partner': {'is_partner': self.partner_id},
                'field_info': self.read()[0],
                'data': record
            }

            return self.env.ref('warranty.action_report_warranty_wizzard') \
                .report_action(self, data=data)


        if self.to_date:
            if self.from_date:
                sql += " where  (requested_date between '" + str(self.from_date) \
                       + "' and '" + str(self.to_date) + "')"
            else:
                sql += " where requested_date <= '" + str(fields.Date.today()) + "'"

            print(sql)
            self.env.cr.execute(sql)
            record = self.env.cr.dictfetchall()

            data = {
                'is_partner': {'is_partner': self.partner_id},
                'field_info': self.read()[0],
                'data': record
            }

            return self.env.ref('warranty.action_report_warranty_wizzard') \
                .report_action(self, data=data)

    def action_print_xls(self):
        temp_list = str(self.product_list.mapped('id'))
        temp_list='('+temp_list[1:-1]+")"
        sql = 'select * from warranty_request'
        if self.partner_id:
            sql += " where customer_id=" + str(self.partner_id.id) + ""
            if self.product_list:
                sql += " and product_id in " + temp_list
            if self.from_date:
                if self.to_date:
                    sql += " and (requested_date  between '" + str(
                        self.from_date) \
                           + "' and '" + str(self.to_date) + "')"
                else:
                    sql += " and (requested_date between '" + str(
                        self.from_date) \
                           + "' and '" + str(fields.Date.today()) + "')"

            self.env.cr.execute(sql)
            record = self.env.cr.dictfetchall()
            print(record)
            data = {
            'id': self.id,
            'model': self._name,
            'warranty_data': record
            }
            return {
            'type': 'ir.actions.report',
            'data': {'model': 'report.wizard',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Warranty XLS',
                     },
            'report_type': 'xlsx'
             }
    def get_xlsx_report(self, data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Warranty XLS')
        headiing = workbook.add_format({'font_size': 20, 'align': 'center', 'bold': True})
        font_1 = workbook.add_format({'font_size': 10, 'align': 'center', 'bold': True})
        sheet.merge_range('A1:N2', 'Product Warranty',headiing)
        row=3
        print(self.partner_id,"ofdj")
        if self.partner_id:

            sheet.write('A' + str(row), "Customer")
            sheet.merge_range('B'+str(row)+':C'+str(row) , self.partner_id.name)
            row += 2
        if self.from_date:
            sheet.write('A'+str(row), "Start Date")
            sheet.merge_range('B' + str(row) + ':C' + str(row), self.from_date)
            row+=2
        if self.to_date:
            sheet.write('A' + str(row), "End Date")
            sheet.merge_range('B' + str(row) + ':C' + str(row), self.to_date)
        if self.product_list:
            product_items =  self.product_list.mapped("display_name")
            print(product_items)



        sheet.merge_range('A'+str(row)+':B'+str(row) , 'Ref no',font_1)
        sheet.merge_range('C'+str(row)+':D'+str(row) , 'Invoice Ref',font_1)
        sheet.merge_range('E'+str(row)+':F'+str(row) ,'Product',font_1)
        sheet.merge_range('G'+str(row)+':H'+str(row), 'Warranty Type',font_1)
        sheet.merge_range('I'+str(row)+':J'+str(row), 'Serial Number',font_1)
        sheet.merge_range('K'+str(row)+':L'+str(row), 'Requested Date',font_1)
        sheet.merge_range('M'+str(row)+':N'+str(row), 'State',font_1)
        row+=1
        for rec in data['warranty_data']:
            sheet.merge_range('A' + str(row) + ':B' + str(row),
                              rec['sequence_number'])
            sheet.merge_range('C' + str(row) + ':D' + str(row),
                              rec['report_invoice_ref'])
            sheet.merge_range('E' + str(row) + ':F' + str(row),
                              rec['report_product'])
            if rec['warranty_type'] == 'service_warranty':
                sheet.merge_range('G' + str(row) + ':H' + str(row),
                                  'Service Warranty')
            if rec['warranty_type'] == 'replacement_warranty':
                sheet.merge_range('G' + str(row) + ':H' + str(row),
                                  'Replacement warranty')
            sheet.merge_range('I' + str(row) + ':J' + str(row),
                             rec['report_serial'])
            sheet.merge_range('K' + str(row) + ':L' + str(row),
                              rec['requested_date'])
            sheet.merge_range('M' + str(row) + ':N' + str(row),
                              rec['state'])
            row+=1





        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()