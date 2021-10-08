import time
from datetime import date, datetime
import pytz
import json
import datetime
import io
from odoo import api, fields, models
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
        temp_list = '('+temp_list[1:-1]+")"
        sql = 'select w.sequence_number,p.display_name,pt.name as product,' \
              ' w.state,am.name as Invoice ,' \
              'pp.warranty_type,w.requested_date, ' \
              'sl.name as Serial from ' \
              'warranty_request as w,res_partner as p ' \
              ', product_product as pp, product_template as pt , ' \
              'account_move as am ' \
              ',stock_production_lot as sl' \
              ' where w.customer_id = p.id and pp.id = w.product_id ' \
              ' and pp.product_tmpl_id = pt.id and am.id=w.invoice_id' \
              ' and sl.id=w.serial_number_id'
        if self.partner_id:
            sql += " and w.customer_id="+str(self.partner_id.id)+""
            if self.product_list:
                sql += " and w.product_id in "+temp_list
            if self.from_date:
                if self.to_date:
                    sql += " and (w.requested_date  between '"\
                         + str(self.from_date)\
                         + "' and '" + str(self.to_date)+"')"
                else:
                    sql += " and (w.requested_date between '" \
                           + str(self.from_date) \
                           + "' and '" + str(fields.Date.today())+"')"

            print(self.partner_id.read()[0])
            self.env.cr.execute(sql)
            record = self.env.cr.dictfetchall()
            print(record)
            # print(self.product_list.read()[0])

            data = {
                'is_partner': {'is_partner': self.partner_id},
                'partner': self.partner_id.read()[0],
                'field_info': self.read()[0],
                'product_list': self.product_list.read(),
                'data': record
            }

            return self.env.ref('warranty.action_report_warranty_wizzard') \
                .report_action(self, data=data)
        if self.product_list:
            print(self.read()[0])
            sql += " and  w.product_id in "+temp_list
            if self.from_date:
                if self.to_date:
                    sql += " and (w.requested_date between  '"\
                         + str(self.from_date)\
                         + "' and '"+str(self.to_date)+"')"
                else:
                    sql += " and (w.requested_date between '" \
                           + str(self.from_date) \
                           + "' and '" + str(fields.Date.today())+"')"
            print(sql)
            self.env.cr.execute(sql)
            record = self.env.cr.dictfetchall()
            print(record)
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
                sql += " and  (w.requested_date between '"+str(self.from_date)\
                         + "' and '" + str(self.to_date)+"')"
            else:
                sql += " and (w.requested_date between '" \
                       + str(self.from_date) \
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
                sql += " and  (w.requested_date between '" \
                       + str(self.from_date) \
                       + "' and '" + str(self.to_date) + "')"
            else:
                sql += " and w.requested_date <= '" \
                       + str(fields.Date.today()) + "'"

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
        temp_list = '('+temp_list[1:-1]+")"
        is_product_list = False
        sql = 'select w.sequence_number,p.display_name,pt.name as product,' \
              ' w.state,am.name as Invoice ,' \
              'pp.warranty_type,w.requested_date, ' \
              'sl.name as Serial from ' \
              'warranty_request as w,res_partner as p ' \
              ', product_product as pp, product_template as pt , ' \
              'account_move as am ' \
              ',stock_production_lot as sl' \
              ' where w.customer_id = p.id and pp.id = w.product_id ' \
              ' and pp.product_tmpl_id = pt.id and am.id=w.invoice_id' \
              ' and sl.id=w.serial_number_id'
        if self.partner_id:
            sql += " and w.customer_id=" + str(self.partner_id.id) + ""
            if self.product_list:
                is_product_list = self.product_list.mapped("display_name")
                sql += " and w.product_id in " + temp_list
            if self.from_date:
                if self.to_date:
                    sql += " and (w.requested_date  between '" + str(
                        self.from_date) \
                           + "' and '" + str(self.to_date) + "')"
                else:
                    sql += " and (w.requested_date between '" + str(
                        self.from_date) \
                           + "' and '" + str(fields.Date.today()) + "')"

            self.env.cr.execute(sql)
            record = self.env.cr.dictfetchall()
            print(record)
            data = {
            'id': self.id,
            'model': self._name,
            'warranty_data': record,
            'form': self.read()[0],
            'product_list': is_product_list
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
        if self.product_list:
            is_product_list = self.product_list.mapped("display_name")
            print(self.read()[0])
            sql += " and  w.product_id in " + temp_list
            if self.from_date:
                if self.to_date:
                    sql += " and (w.requested_date between  '" + str(
                        self.from_date) \
                           + "' and '" + str(self.to_date) + "')"
                else:
                    sql += " and (w.requested_date between '" + str(
                        self.from_date) \
                           + "' and '" + str(fields.Date.today()) + "')"
            print(sql)
            self.env.cr.execute(sql)
            record = self.env.cr.dictfetchall()
            print(record)
            data = {
                'id': self.id,
                'model': self._name,
                'warranty_data': record,
                'form': self.read()[0],
                'product_list': is_product_list
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
        if self.from_date:
            if self.to_date:
                sql += " and  (w.requested_date between '" \
                       + str(self.from_date) \
                       + "' and '" + str(self.to_date) + "')"
            else:
                sql += " and (w.requested_date between '" \
                       + str(self.from_date) \
                       + "' and '" + str(fields.Date.today()) + "')"

            print(sql)
            self.env.cr.execute(sql)
            record = self.env.cr.dictfetchall()
            print(record)
            data = {
                'id': self.id,
                'model': self._name,
                'warranty_data': record,
                'form': self.read()[0],
                'product_list': is_product_list
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
        if self.to_date:
            if self.from_date:
                sql += " and  (w.requested_date between '" \
                       + str(self.from_date) + \
                       "' and '" + str(self.to_date) + "')"
            else:
                sql += " and w.requested_date <= '" + str(fields.Date.today()) \
                       + "'"

            print(sql)
            self.env.cr.execute(sql)
            record = self.env.cr.dictfetchall()
            data = {
                'id': self.id,
                'model': self._name,
                'warranty_data': record,
                'form': self.read()[0],
                'product_list': is_product_list
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
        headiing = workbook.add_format({'font_size': 20, 'align': 'center',
                                        'bold': True})
        font_1 = workbook.add_format({'font_size': 12, 'align': 'center',
                                      'bold': True})
        font_2 = workbook.add_format({'font_size': 12, 'bold': True})
        sheet.set_column(0, 9, 16)
        headiing.set_bg_color('yellow')

        row = 6
        if data['form']['partner_id']:
            sheet.merge_range('A1:G2', 'Product Warranty', headiing)
            sheet.write('A' + str(row), "Customer", font_2)
            sheet.write('B'+str(row), data['form']['partner_id'][1])
            row += 2
        if data['form']['from_date']:
            sheet.write('A' + str(row), "Start Date", font_2)
            sheet.write('B' + str(row), data['form']['from_date'])
            row += 2
            if not data['form']['to_date']:
                sheet.write('A' + str(row), "End Date", font_2)
                sheet.write('B' + str(row),  str(fields.date.today()))
            row += 2
        if data['form']['to_date']:
            sheet.write('A' + str(row), "End Date", font_2)
            sheet.write('B' + str(row), data['form']['to_date'])
            row += 2

        if data['product_list']:
            sheet.write('A' + str(row), "Product", font_2)
            for rec in data['product_list']:
                sheet.write('B' + str(row), rec)
                row += 3
        font_1.set_bg_color('#808080')
        col = 0
        sheet.write(row, col, 'Ref no', font_1)
        col += 1

        sheet.write(row, col, 'Invoice Ref', font_1)
        col += 1
        if not data['form']['partner_id']:
            sheet.write(row, col, 'Customer', font_1)
            col += 1
            sheet.merge_range('A1:H2', 'Product Warranty', headiing)

        sheet.write(row, col, 'Product', font_1)
        col += 1
        sheet.write(row, col, 'Warranty Type', font_1)
        col += 1
        sheet.write(row, col, 'Serial Number', font_1)
        col += 1
        sheet.write(row, col, 'Requested Date', font_1)
        col += 1
        sheet.write(row, col, 'State', font_1)

        row += 1
        for rec in data['warranty_data']:
            col = 0
            sheet.write(row, col, rec['sequence_number'])
            col += 1
            sheet.write(row, col, rec['invoice'])
            col += 1
            if not data['form']['partner_id']:
                sheet.write(row, col, rec['display_name'])
                col += 1
            sheet.write(row, col, rec['product'])
            col += 1
            if rec['warranty_type'] == 'service_warranty':
                sheet.write(row, col, 'Service Warranty')
            if rec['warranty_type'] == 'replacement_warranty':
                sheet.write(row, col, 'Replacement warranty')
            col += 1
            sheet.write(row, col, rec['serial'])
            col += 1
            sheet.write(row, col, rec['requested_date'])
            col += 1
            if rec['state'] == 'draft':
                sheet.write(row, col,
                            'Draft')
            if rec['state'] == 'to approve':
                sheet.write(row, col,
                            'To Approve')
            if rec['state'] == 'approved':
                sheet.write(row, col,
                            'Approved')
            if rec['state'] == 'received':
                sheet.write(row, col, 'Received')
            if rec['state'] == 'done':
                sheet.write(row, col,
                            'Done')
            if rec['state'] == 'cancel':
                sheet.write(row, col,
                            'Cancel')
            row += 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
