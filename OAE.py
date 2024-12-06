import streamlit as st
from openai import OpenAI
import pandas as pd

st.title("Banco de Dados OAE")
st.write(
    "Faça o upload de um arquivo CSV e pergunte o que quiser!"
)

openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Adicione a sua chave da OpenAI API.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    uploaded_file = st.file_uploader(
        "Upload do documento (.csv)", type=("csv")
    )

    # Ask the user for a question via st.text_area.
    question = st.text_area(
        "Faça uma pergunta!",
        placeholder="Quantos viadutos há no banco de dados?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:

        if uploaded_file.name.endswith(".csv"):
            # Load CSV content.
            df = pd.read_csv(uploaded_file)
            document = df.to_string(index=False) 
        else:
            # Load text content.
            document = uploaded_file.read().decode()

        messages = [
            {
                "role": "user",
                "content": f"Aqui está o documento: {document} \n\n---\n\n {question}",
            }
        ]

        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
        )

        st.write_stream(stream)
