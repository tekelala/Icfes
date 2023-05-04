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
            try:
                text = extract_text_from_pdf(uploaded_file)
            except Exception as e:
                st.error(f"Error reading file {uploaded_file.name}: {e}")
                continue

            # Save the text to a .txt file
            try:
                with open(f'{uploaded_file.name}.txt', 'w') as f:
                    f.write(text)
            except Exception as e:
                st.error(f"Error writing to file {uploaded_file.name}.txt: {e}")
                continue

            # Classify the PDF based on keywords
            for category, category_keywords in keywords.items():
                if any(keyword in text for keyword in category_keywords):
                    # Move the .txt file to a directory named after the category
                    os.makedirs(category, exist_ok=True)
                    try:
                        os.rename(f'{uploaded_file.name}.txt', f'{category}/{uploaded_file.name}.txt')
                    except Exception as e:
                        st.error(f"Error moving file to category {category}: {e}")
                    break

        # Allow the user to select a category and a .txt file within that category
        category = st.selectbox('Select a category', list(keywords.keys()))
        
        # Check if the directory for the selected category exists
        if os.path.isdir(category):
            file = st.selectbox('Select a file', os.listdir(category))
        else:
            st.write(f"No files in category {category}")
            return  # Exit the function if the directory does not exist

        if st.button('Proponer respuesta'):
            # Propose a response using GPT-3.5
            with open(f'{category}/{file}', 'r') as f:
                text = f.read()
            try:
                response = propose_response(text)
                st.write(f'Proposed response for {file} in category {category}: {response}')
            except Exception as e:
                st.error(f"Error generating response: {e}")

def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfFileReader(uploaded_file)
    text = ''
    for page_num in range(pdf_reader.numPages):
        page_obj = pdf_reader.getPage(page_num)
        text += page_obj.extractText()
    return text

def propose_response(text):
    # Make a request to the GPT-3.5 API
    try:
        response = requests.post(GPT_API_URL, json={'text': text})
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        raise SystemExit(http_err)
    except Exception as err:
        raise SystemExit(err)
    proposed_response = response.json()['response']
    return proposed_response

if __name__ == "__main__":
    main()
