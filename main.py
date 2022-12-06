from fpdf import FPDF
import pandas as pd
from os import path

data_dir = path.join(path.curdir, 'data')

pdf = FPDF(orientation='P', unit='mm', format='A4')

pdf.add_page()

pdf.set_font(family='Times', style='B', size=12)
pdf.cell(w=0, h=12, txt='Hello There!', align='L', ln=1, border=1)
pdf.set_font(family='Times', size=10)
pdf.cell(w=0, h=12, txt='Hi There!', align='L', ln=1, border=1)

df = pd.read_csv(path.join(data_dir, 'topics.csv'))
page_counter = 1
for index, row in df.iterrows():
    for page in range(row['Pages']):
        pdf.add_page()
        pdf.set_font(family='Times', style='B', size=24)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(w=0, h=12, txt=row['Topic'], align='L', ln=1)
        pdf.line(x1=10, y1=21, x2=200, y2=21)


pdf.output('output.pdf')

print(pdf)