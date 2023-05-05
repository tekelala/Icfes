import streamlit as st
from PyPDF2 import PdfReader
import requests
import io
import os
import openai

# Function to get the model completion
def get_completion(prompt):
    # Set the OpenAI API key from the environment variable
    openai_api_key = os.getenv('OPENAI_API_KEY')
    
    # Check if the API key is set
    if not openai_api_key:
        return "API key for OpenAI not found. Please set the 'OPENAI_API_KEY' environment variable."

    openai.api_key = openai_api_key
    messages = [{"role": "user", "content": prompt}]
        
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.5, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

# Keywords for each category
keywords = {
    'Quejas y Reclamos': ['Queja', 'Reclamo'],
    'Derechos de Petición': ['Derecho de Petición', 'Peticion'],
    'Tutelas': ['Tutela', 'Tutelas'],
    'Requerimientos': ['contraloria', 'procuraduria']
}

def main():
    st.image("header.png")  # replace with the path to your header image
    st.title("ICETEX")
    st.write("Bienvenido al sistema de respuestas asistidas de ICETEX")
    st.write("""Somos una entidad que reconoce y valora la calidad de la educación como la clave para construir escenarios de inclusión social, aportar a la competitividad económica y laboral del país y fortalecer los espacios comunes de aprendizaje, como las aulas de clase.
Nuestra esencia es transformar los resultados de las pruebas de Estado en una oportunidad para identificar las necesidades de aprendizaje y apropiación de competencias de las personas, en cualquier etapa de su vida.""")


    col1, col2 = st.columns(2)
    col1.image("SG.jpg")  # replace with the path to your profile picture
    col2.write("Hola Luisa, estos son los documentos para hoy")
    
    uploaded_files = st.file_uploader("Upload PDF Files", type='pdf', accept_multiple_files=True)

    if uploaded_files is not None:
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
    file = None
    if os.path.isdir(category):
        file = st.selectbox('Select a file', os.listdir(category))
    else:
        st.write(f"No files in category {category}")

    if file and st.button('Proponer respuesta'):
        with open(f'{category}/{file}', 'r') as f:
            text = f.read()
        try:
            # Call the function to get the completion
            prompt = f"""
            Eres un excelente abogado del ICFES respondiendo {category} el texto que debes responder es {text}
            """
            with st.spinner('Generando una propuesta de respuesta...'):
                st.session_state.content = get_completion(prompt)
            st.text_area('Proposed response', value=st.session_state.content, height=200)
            if st.download_button('Descargar', st.session_state.content, file_name='response.txt', mime='text/plain'):
                st.success('Response downloaded')
            if st.button('Enviar Respuesta'):
                st.success('Response sent')
        except Exception as e:
            st.error(f"Error generating response: {e}")

def extract_text_from_pdf(uploaded_file):
    pdf_reader = PdfReader(uploaded_file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text
if __name__ == "__main__":
    main()