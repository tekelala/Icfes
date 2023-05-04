import streamlit as st
import os
import PyPDF2
from collections import defaultdict

# Directory containing the PDF files
pdf_dir = '/path/to/your/pdf/files'

# Keywords for each category
keywords = {
    'Quejas': ['keyword1', 'keyword2'],
    'Derechos': ['keyword3', 'keyword4'],
    'Tutelas': ['keyword5', 'keyword6'],
    'Requerimientos': ['keyword7', 'keyword8']
}

# Counts for each category
counts = defaultdict(int)

# List of files in each category
files = defaultdict(list)

def main():
    st.title("PDF Classification App")
    
    if st.button('Iniciar'):
        # Read all PDF files in the directory
        for filename in os.listdir(pdf_dir):
            if filename.endswith('.pdf'):
                file_path = os.path.join(pdf_dir, filename)
                text = extract_text_from_pdf(file_path)
                
                # Classify the PDF based on keywords
                for category, category_keywords in keywords.items():
                    if any(keyword in text for keyword in category_keywords):
                        counts[category] += 1
                        files[category].append(filename)
                        break

        # Display the count of PDFs in each category
        for category, count in counts.items():
            st.write(f'{category}: {count} files')

        # Allow the user to select a PDF from a category
        category = st.selectbox('Select a category', list(keywords.keys()))
        file = st.selectbox('Select a file', files[category])

        if st.button('Proponer respuesta'):
            # Propose a response (you can replace this with your own logic)
            st.write(f'Proposed response for {file} in category {category}')

def extract_text_from_pdf(file_path):
    pdf_file_obj = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
    text = ''
    for page_num in range(pdf_reader.numPages):
        page_obj = pdf_reader.getPage(page_num)
        text += page_obj.extractText()
    pdf_file_obj.close()
    return text

if __name__ == "__main__":
    main()
