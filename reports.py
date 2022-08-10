from config import app
import mimetypes
from urllib import response

from models import *
from fpdf import FPDF
from flask import request,flash,render_template,session
from flask.wrappers import Response
from sqlalchemy import and_
@app.route("/soldcarsreport")
def soldcarsreport():
        pdf=FPDF(orientation='l')
        pdf.add_page()
        page_width=pdf.w - 2 * pdf.l_margin
        pdf.set_font('Times','B',14.0)
        pdf.cell(page_width,0.0,'SOLD CARS',align='C')
        pdf.ln(10)
        col_width=page_width/7
        pdf.ln(1)
        pdf.cell(col_width+10,4,'Number plate',border=1)
        pdf.cell(col_width,4,'Origin',border=1)
        pdf.cell(col_width-10,4,'Model',border=1)
        pdf.cell(col_width,4,'Fuel',border=1)
        pdf.cell(col_width,4,'Steering',border=1)
        pdf.cell(col_width,4,'Logbook number',border=1)        
        pdf.cell(col_width-10,4,'Engine',border=1)
        pdf.cell(col_width,4,'Price',border=1)
        pdf.ln(4)
        pdf.set_font('Courier','',12)
        th=pdf.font_size
        results=add_car.query.all()
        for row in results:
                pdf.cell(col_width+10,th,row.number_plate,border=1)
                pdf.cell(col_width,th,row.origin[:10],border=1)
                pdf.cell(col_width-10,th,row.model ,border=1)
                pdf.cell(col_width,th,str(row.fuel),border=1)
                pdf.cell(col_width,th,row.steering[:10],border=1)
                pdf.cell(col_width,th,row.logbook_number[:10],border=1)
                pdf.cell(col_width-10,th,row.engine[:10],border=1)
                pdf.cell(col_width+10,th,str(row.price),border=1)
                
                pdf.ln(th)

        pdf.ln(10)
        pdf.set_font('Times','',10)
        pdf.cell(page_width,0.0,'end of report',align='C')
        return Response(pdf.output(dest='S').encode('latin-1'),mimetype='application/pdf',headers={'Content-Disposition':'attachment;filename=report.pdf'})



@app.route("/hiredcarsreport")
def hiredcarsreport():
        pdf=FPDF(orientation='l')
        pdf.add_page()
        page_width=pdf.w - 2 * pdf.l_margin
        pdf.set_font('Times','B',14.0)
        pdf.cell(page_width,0.0,'HIRED CARS',align='C')
        pdf.ln(10)
        col_width=page_width/6
        pdf.ln(1)
        pdf.cell(col_width+10,4,'Number plate',border=1)
        pdf.cell(col_width,4,'Username',border=1)
        pdf.cell(col_width-10,4,'Hiring Date',border=1)
        pdf.cell(col_width,4,'Returning Date',border=1)
        pdf.cell(col_width,4,'Period',border=1)
        pdf.cell(col_width,4,'Amount',border=1)
        pdf.ln(4)
        pdf.set_font('Courier','',12)
        th=pdf.font_size
        results=hired_car_details.query.all()
        for row in results:
                pdf.cell(col_width+10,th,row.number_plate,border=1)
                pdf.cell(col_width,th,row.username[:10],border=1)
                pdf.cell(col_width-10,th,row.hiring_date,border=1)
                pdf.cell(col_width,th,str(row.returning_date),border=1)
                pdf.cell(col_width,th,row.period[:10],border=1)
                pdf.cell(col_width,th,str(row.amount),border=1)
                
                pdf.ln(th)

        pdf.ln(10)
        pdf.set_font('Times','',10)
        pdf.cell(page_width,0.0,'end of report',align='C')
        return Response(pdf.output(dest='S').encode('latin-1'),mimetype='application/pdf',headers={'Content-Disposition':'attachment;filename=report.pdf'})

# @app.route("/hiredcarsreport")
# def hiredcarsreport():
#         pdf=FPDF(orientation='l')
#         pdf.add_page()
#         page_width=pdf.w - 2 * pdf.l_margin
#         pdf.set_font('Times','B',14.0)
#         pdf.cell(page_width,0.0,'HIRED CARS',align='C')
#         pdf.ln(10)
#         col_width=page_width/6
#         pdf.ln(1)
#         pdf.cell(col_width+10,4,'Number plate',border=1)
#         pdf.cell(col_width,4,'Username',border=1)
#         pdf.cell(col_width-10,4,'Hiring Date',border=1)
#         pdf.cell(col_width,4,'Returning Date',border=1)
#         pdf.cell(col_width,4,'Period',border=1)
#         pdf.cell(col_width,4,'Amount',border=1)
#         pdf.ln(4)
#         pdf.set_font('Courier','',12)
#         th=pdf.font_size
#         results=hired_car_details.query.all()
#         for row in results:
#                 pdf.cell(col_width+10,th,row.number_plate,border=1)
#                 pdf.cell(col_width,th,row.username[:10],border=1)
#                 pdf.cell(col_width-10,th,row.hiring_date,border=1)
#                 pdf.cell(col_width,th,str(row.returning_date),border=1)
#                 pdf.cell(col_width,th,row.period[:10],border=1)
#                 pdf.cell(col_width,th,str(row.amount),border=1)
                
#                 pdf.ln(th)

#         pdf.ln(10)
#         pdf.set_font('Times','',10)
#         pdf.cell(page_width,0.0,'end of report',align='C')
#         return Response(pdf.output(dest='S').encode('latin-1'),mimetype='application/pdf',headers={'Content-Disposition':'attachment;filename=report.pdf'})

