import streamlit as st
import PyPDF2
import requests
import io
import os

# Keywords for each category
keywords = {
    'Quejas': ['Queja', 'Reclamo'],
    'Derechos': ['Derecho de Petición', 'Peticion'],
    'Tutelas': ['Tutela', 'Tutelas'],
    'Requerimientos': ['contraloria', 'procuraduria']
}

# Your GPT-3.5 API URL
GPT_API_URL = 'http://example.com/api/gpt-3.5'

def main():
    st.title("PDF Classification App")

    if st.button('Iniciar'):
        uploaded_files = st.file_uploader("Upload PDF Files", type='pdf', accept_multiple_files=True)

        for uploaded_file in uploaded_files:
            text = extract_text_from_pdf(uploaded_file)
            
            # Save the text to a .txt file
            with open(f'{uploaded_file.name}.txt', 'w') as f:
                f.write(text)

            # Classify the PDF based on keywords
            for category, category_keywords in keywords.items():
                if any(keyword in text for keyword in category_keywords):
                    # Move the .txt file to a directory named after the category
                    os.makedirs(category, exist_ok=True)
                    os.rename(f'{uploaded_file.name}.txt', f'{category}/{uploaded_file.name}.txt')
                    break

        # Display the categories and the .txt files in each category
        for category in keywords.keys():
            st.write(f'{category}:')
            for file in os.listdir(category):
                st.write(file)

        # Allow the user to select a category and a .txt file within that category
        category = st.selectbox('Select a category', list(keywords.keys()))
        file = st.selectbox('Select a file', os.listdir(category))

        if st.button('Proponer respuesta'):
            # Propose a response using GPT-3.5
            with open(f'{category}/{file}', 'r') as f:
                text = f.read()
            response = propose_response(text)
            st.write(f'Proposed response for {file} in category {category}: {response}')

def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfFileReader(uploaded_file)
    text = ''
    for page_num in range(pdf_reader.numPages):
        page_obj = pdf_reader.getPage(page_num)
        text += page_obj.extractText()
    return text

def propose_response(text):
    # Make a request to the GPT-3.5 API
    response = requests.post(GPT_API_URL, json={'text': text})
    proposed_response = response.json()['response']
    return proposed_response

if __name__ == "__main__":
    main()