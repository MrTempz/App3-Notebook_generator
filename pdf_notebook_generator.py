from fpdf import FPDF
import pandas as pd
from os import path
from enum import Enum

class OverlayStyles(Enum):
    GRID = 1
    LINES_BIG = 2
    LINES_SMALL = 3

def add_front_page(pdf, front_page):
    pdf.add_page()


    pdf.set_font(family='Times', style='B', size=24)
    pdf.cell(w=0, h=12, txt=front_page[0], align='C', ln=1)
    if len(front_page) > 1:
        pdf.set_font(family='Times', style='I', size=12)
        pdf.cell(w=0, h=12, txt=front_page[1], align='C', ln=1) 
        if len(front_page) > 2:
            for text in front_page[2:]:
                pdf.set_font(family='Times', size=10)
                pdf.cell(w=0, h=12, txt=text, align='C', ln=1) 

def add_lines(pdf, page_start, lines_size):
    width = 0.2

    if lines_size == OverlayStyles.LINES_BIG:
        step = 10
        size_change = False
    elif lines_size == OverlayStyles.LINES_SMALL:
        step = 5
        size_change = True

    for y in range(page_start, 292, step):
        pdf.set_line_width(width=width)
        pdf.line(x1=10, y1=y, x2=200, y2=y)
        width = 0.1 if width == 0.2 and size_change else 0.2

def add_grid(pdf, page_start):
    add_lines(pdf, page_start, OverlayStyles.LINES_SMALL)
    width = 0.2
    for x in range(10, 201, 5):
        pdf.set_line_width(width=width)
        pdf.line(x1=x, y1=page_start, x2=x, y2=291)
        width = 0.1 if width == 0.2 else 0.2

def add_overlay(pdf, overlay_style, page_start):
    if overlay_style== OverlayStyles.GRID:
        add_grid(pdf, page_start)
    elif overlay_style in (OverlayStyles.LINES_BIG, OverlayStyles.LINES_SMALL):
        add_lines(pdf, page_start, overlay_style)

def add_header(pdf, topic):
    pdf.set_font(family='Times', style='B', size=24)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(w=0, h=12, txt=topic, align='L', ln=1)

def add_footer(pdf, topic, page_counter, footer_placement):
    pdf.ln(footer_placement)
    pdf.set_font(family='Times', style='I', size=8)
    pdf.set_text_color(180, 180, 180)
    pdf.cell(w=0, h=12, txt=str(page_counter), align='L')
    pdf.cell(w=0, h=12, txt=topic, align='R')

def add_pages(pdf, topic, pages, overlay_style, page_counter):
    pdf.add_page()
    page_counter += 1

    add_header(pdf, topic)
    add_footer(pdf, topic, page_counter, footer_placement=265)

    add_overlay(pdf, overlay_style, page_start=21)
    for i in range(pages-1):
        pdf.add_page()
        page_counter += 1
        
        add_footer(pdf, topic, page_counter, footer_placement=277)

        add_overlay(pdf, overlay_style, page_start=11)

def generate_notebook(notebook_df, output_file, overlay_style, front_page):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=False, margin=0)

    add_front_page(pdf, front_page)
    
    page_counter = 1
    for index, row in notebook_df.iterrows():
        try:
            topic_overlay = OverlayStyles[row['Style']]
        except KeyError:
            topic_overlay = overlay_style
        add_pages(pdf, row['Topic'], row['Pages'], topic_overlay, page_counter)
        page_counter += row['Pages']
      
    pdf.output(output_file)

if __name__ == '__main__':

    csv_file = path.join(path.curdir, 'data', 'topics_template.csv')
    df = pd.read_csv(csv_file, sep=';')
    output_file = 'output.pdf'
    front_page = ['Hello', 'Hi There!', "Let's create ourselves a notebook", 
        'testy testy testy test', 'one more for good meassure']

    generate_notebook(notebook_df=df, output_file=output_file, 
         overlay_style=OverlayStyles.LINES_SMALL, front_page=front_page)
