import streamlit as st
import pandas as pd
from os import path
import pdf_notebook_generator as png

st.set_page_config(layout='wide')

data_dir = path.join(path.curdir, 'data')

st.title("Notebook generator")
st.header("Generate your own notebook")

col1, empty_col, col2 = st.columns([1.5, 0.5, 1.5])

with col1:
    content = f"""
    In order to create your own notebook, please upload a CSV file with values separated by ';'.\n
    Column names should be:\n
    Order;Topic;Pages[;Style]\n\n
    Note that the Style is optional, you can choose style for the whole notebook with below dropdown. 
    Style from CSV file will overwrite overal style of the notebook.\n
    Style has to follow a certain naming conventions, there are {len(png.OverlayStyles)} 
    available styles: {', '.join([style.name for style in png.OverlayStyles])}\n
    """
    st.write(content)

with col2:
    st.write('Example of CSV file:')

    template_df = pd.read_csv(path.join(data_dir, 'topics_template.csv'), sep=';')
    st.table(template_df)

overlay_style = st.selectbox(label='Choose style for your notebok', options=[style.name for style in png.OverlayStyles])

uploaded_file = st.file_uploader(label='Upload your CSV file', type='csv')

if uploaded_file:
    df = pd.read_csv(uploaded_file, sep=';')
    file_name = uploaded_file.name
    simple_name = file_name.replace('.csv', '')
    notebook_name = file_name.replace('.csv', '.pdf')
    st.table(df)
    
    print(png.OverlayStyles[overlay_style])
    png.generate_notebook(notebook_df=df, output_file=notebook_name, overlay_style=png.OverlayStyles[overlay_style], 
        front_page=[simple_name.replace('_', '').title(), 'Hello there!',
        f'This is a notebook devoted to {simple_name.replace("_", " ")}', 'Have fun using it!'])
    
    with open(notebook_name, 'rb') as pdf_file:
        PDFbyte = pdf_file.read()

    st.download_button(label='Download notebook', data=PDFbyte, file_name=notebook_name)
    


