from fpdf import FPDF
import pandas as pd
from os import path

data_dir = path.join(path.curdir, 'data')

pdf = FPDF(orientation='P', unit='mm', format='A4')
pdf.set_auto_page_break(auto=False, margin=0)

pdf.add_page()

pdf.set_font(family='Times', style='B', size=12)
pdf.cell(w=0, h=12, txt='Hello There!', align='L', ln=1, border=1)
pdf.set_font(family='Times', size=10)
pdf.cell(w=0, h=12, txt='Hi There!', align='L', ln=1, border=1)

df = pd.read_csv(path.join(data_dir, 'topics.csv'))
page_counter = 1
for index, row in df.iterrows():
    pdf.add_page()
    page_counter += 1

    pdf.set_font(family='Times', style='B', size=24)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(w=0, h=12, txt=row['Topic'], align='L', ln=1)

    pdf.ln(265)
    pdf.set_font(family='Times', style='I', size=8)
    pdf.set_text_color(180, 180, 180)
    pdf.cell(w=0, h=12, txt=str(page_counter), align='L')
    pdf.cell(w=0, h=12, txt=row['Topic'], align='R')
    width = 0.2
    for y in range(21, 292, 5):
        pdf.set_line_width(width=width)
        pdf.line(x1=10, y1=y, x2=200, y2=y)
        width = 0.1 if width == 0.2 else 0.2
    
    width = 0.2
    for x in range(10, 201, 5):
        pdf.set_line_width(width=width)
        pdf.line(x1=x, y1=21, x2=x, y2=291)
        width = 0.1 if width == 0.2 else 0.2


    for page in range(row['Pages']-1):
        pdf.add_page()
        page_counter += 1
        
        pdf.ln(279)
        pdf.set_font(family='Times', style='I', size=8)
        pdf.set_text_color(180, 180, 180)
        pdf.cell(w=0, h=12, txt=str(page_counter), align='L')
        pdf.cell(w=0, h=12, txt=row['Topic'], align='R')
        width = 0.2
        for y in range(11, 292, 5):
            pdf.set_line_width(width=width)
            pdf.line(x1=10, y1=y, x2=200, y2=y)
            width = 0.1 if width == 0.2 else 0.2
        
        width = 0.2
        for x in range(10, 201, 5):
            pdf.set_line_width(width=width)
            pdf.line(x1=x, y1=11, x2=x, y2=291)
            width = 0.1 if width == 0.2 else 0.2

pdf.output('output.pdf')

print(pdf)